# -*- coding: utf-8 -*-
{
    "name": "delivery order in invoice",
    "version": "1.0",
    "description": """Delivery details of the invoice""",
    "sequence": "2",
    "depends": ["base", "sale","purchase" ],
    'data': [
        'views/delivery_detail_views.xml',
    ],
    "application": True,
    "installable": True,

    'author': 'Cybrosys',

}