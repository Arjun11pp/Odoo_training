# -*- coding: utf-8 -*-
{
    "name": "point of sale custom",
    "depends": ['point_of_sale','base','sale'],
    "application": True,
    "installable": True,
    "sequence": "1",
    'data': [
        'views/product_template_view.xml',
'views/res_config_settings_views.xml',
        ],
    'assets': {

        'point_of_sale._assets_pos': [
            'point_of_sale_custom/static/src/js/discount_limit.js',
       'point_of_sale_custom/static/src/xml/pos_order_line.xml',


   ],

    },
'license': 'LGPL-3',
        'author': 'Cybrosys',
}



