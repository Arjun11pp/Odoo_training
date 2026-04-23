# -*- coding: utf-8 -*-
{
    "name": "sale Order custom",
    "depends": ["base","sale",],
    "application": True,
    "installable": True,
    "sequence": "2",
    'data': [
        'views/sale_order_statewise_view.xml',
            'views/sale_order_custom_view.xml',

        ],
'license': 'LGPL-3',
}
