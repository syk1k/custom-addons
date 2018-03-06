# -*- coding: utf-8 -*-
import requests

from odoo import models, fields, api


class Moodle(models.Model):
    """This is the class that generate the moodle table in the database.
     It's used to store the username, email and Token"""
    _name = 'odoo.moodle'
    _description = 'Moodle Odoo Version 11.0'
    username = fields.Char()
    token = fields.Char(string='Moodle Token', help="If you don't have a token make sure you get one.")


    def configure(self):
        """Configure Moodle with this function"""

        '''The method makes a test to get the site info'''
        domain = 'http://localhost:8888'
        webservice_url = '/webservice/rest/server.php?'
        parameters = {
            'wstoken': self.token,
            'wsfunction': 'core_webservice_get_site_info',
            'moodlewsrestformat': 'json'
        }
        request = requests.get(url=domain + webservice_url, params=parameters)
        request = request.json()

        if 'exception' in request:
            if request['exception'] == "moodle_exception":
                if request['errorcode'] == 'invalidtoken':
                    return self._reopen_form()
                    
    
    @api.model
    def create(self, vals):
        self.search([]).unlink()
        vals['id']=1
        print(vals)
        return super(Moodle, self).create(vals)


    @api.multi
    def _reopen_form(self):
        self.ensure_one()
        window = {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id':  self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
        return window



class Category(models.TransientModel):
    """ This model creates a table to temporary store new created categories."""

    _name = 'moodle.category'
    _description = 'Moodle Category Table'

    categories = [
        ('0', 'Top'),
    ]

    category = fields.Selection(string='Category', selection=categories, default=0)
    name = fields.Char(string='Name')
    description = fields.Html(string='Description')


    @api.model
    def create(self, vals):
        self.create_category(vals)
        return super(Category, self).create(vals)


    def create_category(self,vals):
        categories = {
            "categories[0][name]": vals['name'],
            "categories[0][parent]": vals['category'],
            "categories[0][description]": vals['description'],
            "categories[0][descriptionformat]": 1
        }

        token = self.env['odoo.moodle'].search([('create_uid', '=', self.env.user.id)]).token

        domain = "http://localhost:8888"
        webservice_url = "/webservice/rest/server.php?"
        parameters = {
            "wstoken": token,
            'wsfunction': 'core_course_create_categories',
            'moodlewsrestformat': 'json'
        }
        request = requests.request("POST", url=domain + webservice_url, params=parameters, data=categories)
        request = request.json()
        print(request)

        print(token)
        print(type(categories["categories[0][parent]"]))
        print(categories)





class Course(models.TransientModel):
    _name = 'moodle.course'
    _description = 'Moodle Course Table'

    categories = [
        ('1', 'Miscellaneous'),
    ]

    course_id = fields.Integer()
    category = fields.Selection(string='Category', selection=categories, default='1')
    fullname = fields.Char(string='Full Name')
    shortname = fields.Char(string='Short Name')
    date_start = fields.Datetime(string='Start Date')
    date_end = fields.Datetime(string='End Date')
    summary = fields.Html(string='Summary')

    @api.multi
    def _reopen_form(self):
        window = {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
        }
        return window

    @api.model
    def create(self, vals):
        self.create_course(vals)
        return super(Course, self).create(vals)

    def create_course(self, vals):
        courses = {
            "courses[0][fullname]": vals['fullname'],
            "courses[0][shortname]": vals['shortname'],
            "courses[0][categoryid]": vals['category'],
            "courses[0][summary]": vals['summary'],
            #"courses[0][startdate]": self.date_start,
            #"courses[0][enddate]": self.date_end,
        }

        token = self.env['odoo.moodle'].search([('create_uid', '=', self.env.user.id)]).token


        domain = "http://localhost:8888"
        webservice_url = "/webservice/rest/server.php?"
        parameters = {
            "wstoken": token,
            'wsfunction': 'core_course_create_courses',
            'moodlewsrestformat': 'json'
        }
        request = requests.request("POST", url=domain + webservice_url, params=parameters, data=courses)
        request = request.json()
        print(request)

        if 'exception' in request:
            if request['exception']=='webservice_access_exception':
                if request['errorcode']=='accessexception':
                    print('error')
                    return self._reopen_form()


    def update_course(self, vals):
        pass


    def get_courses(self):
        token = self.env['odoo.moodle'].search([('create_uid', '=', self.env.user.id)]).token
        domain = "http://localhost:8888"
        webservice_url = "/webservice/rest/server.php?"
        parameters = {
            "wstoken":token,
            'wsfunction': 'core_course_get_courses',
            'moodlewsrestformat': 'json'
            }
        request = requests.get(url=domain+webservice_url, params=parameters)
        request = request.json()

        print(request)

        for req in request:
            try:
                self.create({
                    'id': req['id'], 
                    'category':req['categoryid'],
                    'fullname':req['fullname'], 
                    'shortname':req['shortname'],
                    'summary': req['summary']
                    }
                )
            except Exception:
                print('Course not created')

    
    def print_something_for_test(self):
        print('Message from the button in the Header Refresh')

class Database(models.TransientModel):
    _name = "moodle.database"
    _description = "Used to refresh the database"

    data_base_id = fields.Integer(string="Database")