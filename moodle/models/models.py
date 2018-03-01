# -*- coding: utf-8 -*-
import string

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

        if 'siteurl' in request:
            if request['siteurl'] == domain:
                print('Hello')
        elif 'exception' in request:
            if request['exception'] == "moodle_exception":
                if request['errorcode'] == 'invalidtoken':
                    print(request['message'])
                    print('Make sure you enter the correct token')
                    print("If you don't have any token yet refer to moodle"
                          + "administrator to find out how to get one ")
            elif request['exception'] == "webservice_access_exception":
                if request['errorcode'] == "accessexception":
                    print(request['message'])
                    print("Check wether your token has the access to view the site info")
                    print("For more information about token accesses refer to your moodle "
                          + "administrator")





class Category(models.TransientModel):
    """ This model creates a table to temporary store new created categories."""

    _name = 'moodle.category'
    _description = 'Moodle Category Table'

    categories = [
        (0, 'Top'),
    ]

    category = fields.Selection(string='Category', selection=categories, default=0)
    name = fields.Char(string='Name')
    id_number = fields.Char(string='ID Number')
    description = fields.Html(string='Description')




    def create_category(self):
        categories = {
            "categories[0][name]": self.name,
            "categories[0][parent]": self.category,
            "categories[0][idnumber]": self.id_number,
            "categories[0][description]": self.description,
            "categories[0][descriptionformat]": 1
        }

        token = self.env['odoo.moodle'].search([('id', '=', 6)]).token

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



class Course(models.TransientModel):
    _name = 'moodle.course'
    _description = 'Moodle Course Table'

    categories = [
        (1, 'Miscellaneous'),
    ]

    category = fields.Selection(string='Category', selection=categories, default=1)
    fullname = fields.Char(string='Full Name')
    shortname = fields.Char(string='Short Name')
    date_start = fields.Datetime(string='Start Date')
    date_end = fields.Datetime(string='End Date')
    summary = fields.Html(string='Summary')


    def create_course(self):
        courses = {
            "courses[0][fullname]": self.fullname,
            "courses[0][shortname]": self.shortname,
            "courses[0][categoryid]": self.category,
            "courses[0][summary]": self.summary,
            "courses[0][startdate]": self.date_start,
            "courses[0][enddate]": self.date_end,
        }

        token = self.env['odoo.moodle'].search([('id', '=', 6)]).token


        domain = "http://localhost:8888"
        webservice_url = "/webservice/rest/server.php?"
        parameters = {
            "wstoken": token,
            'wsfunction': 'core_course_create_courses',
            'moodlewsrestformat': 'json'
        }
        # request = requests.request("POST", url=domain + webservice_url, params=parameters, data=courses)
        # request = request.json()
        #
        # print(self.env.user.name)
        # print(courses["courses[0][fullname]"])

        print(token)