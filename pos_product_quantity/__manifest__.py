# -*- coding: utf-8 -*-

{
    'name': "POS product quantity",
    'version': '19.0.1',
     'category': 'sale',
    'sequence': 2,
    'summary': " Product available quantity in POS",
    'description': "Product available quantity in POS ",
    'application' : True,
    'installable': True,
    'depends': ['base','point_of_sale'],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    "assets": {
        'point_of_sale._assets_pos': [
            'pos_product_quantity/static/src/js/product_card.js',
            'pos_product_quantity/static/src/xml/product_card.xml',
        ],
    },

    'author': 'Cybrosys',
    'license': 'LGPL-3',

}