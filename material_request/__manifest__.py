# -*- coding: utf-8 -*-
{
    "name": "Material Request",
    "depends": ["base","sale",'purchase','hr'],
    "application": True,
    "installable": True,
    "sequence": "2",
    'data': [
        'security/material_request_access_groups.xml',
        'security/ir.model.access.csv',

        'views/material_request_view.xml',
        'views/menu_list.xml',


    ]

}