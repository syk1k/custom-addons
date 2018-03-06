# -*- coding: utf-8 -*-
{
    'name': "Moodle",
    'summary': 'Manage Moodle From Here.',
    'author': "Kalamar",
    'website': "http://www.kalamar.tg",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','web'],

    'qweb': [
        #'static/src/xml/*.xml',
        'views/templates.xml'
    ],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'views/list_view.xml',
        'views/wizard.xml',
        'views/moodle_menu.xml',
        'views/tree_view_asset.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],

    # Installation information
    'application': True,
    'auto_install': False,
    'installable': True,
}