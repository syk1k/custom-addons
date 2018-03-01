# -*- coding: utf-8 -*-
import requests

from odoo.odoo import models, fields, api


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
