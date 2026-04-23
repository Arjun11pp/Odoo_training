# -*- coding: utf-8 -*-
{
    "name": "Specific customer",
    "version": "1.0",
    "description": """Select Customer""",
    "sequence": "2",
    "depends": ["base", "sale_management", 'purchase','point_of_sale'],
    'data': [
        # 'views/res_config_settings_views.xml',
        'views/pos_config_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'specific_customer/static/src/js/print_limit.js',
        ],
    },
    "application": True,
    "installable": True,
    'license': 'LGPL-3',
    'author': 'Cybrosys',
}