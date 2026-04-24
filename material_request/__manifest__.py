# -*- coding: utf-8 -*-
{
    "name": "Material Request",
    "depends": ["base", "sale", 'purchase', 'hr'],
    "application": True,
    "installable": True,
    "sequence": "2",
    'data': [
        'security/material_request_access_groups.xml',
        'security/ir.model.access.csv',
        'views/website_view.xml',
        'views/material_request_view.xml',
        'views/menu_list.xml',

    ],
    'assets': {
        'web.assets_frontend': [
            'material_request/static/src/js/custom.js',
            'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css',
            'material_request/static/src/js/select2.js',

        ]},
    'author': 'Cybrosys',
    'license': 'LGPL-3',

}
