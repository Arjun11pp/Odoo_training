# -*- coding: utf-8 -*-
{
    "name": "customer sale orders",
    "version": "1.0",
    "description": """ display customer sale orders """,
    "sequence": "2",
    "depends": ["base",'sale'],
    "data":[
        'views/res_users_view.xml',
    ],


    "application": True,
    "installable": True,
    'author': 'Cybrosys',
}