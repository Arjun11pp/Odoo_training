# -*- coding: utf-8 -*-
{
    "name": "internal transfer validation",
    "summary": "Internal transfer validation",
    "version": "1.0",
    "description": """Internal transfers need dual validation""",
    "sequence": "2",
    "depends": ["base","stock"],
    'data': [
        'security/groups.xml',
    'views/stock_picking_inherit.xml'
    ],
    "application": True,
    "installable": True,
    'license': 'LGPL-3',
    'author': 'Cybrosys',

}