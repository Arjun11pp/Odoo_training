# -*- coding: utf-8 -*-
{
    "name": "delivery remarks",
    "version": "1.0",
    "description": """delivery remarks""",
    "sequence": "2",
    "depends": ["base","sale_management"],
    'data': [
        'views/sale_order_views.xml',
        'views/res_partner_views.xml',
    ],
    "application": True,
    "installable": True,

    'author': 'Cybrosys',

}