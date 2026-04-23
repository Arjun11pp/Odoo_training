# -*- coding: utf-8 -*-
{
    "name": "Product fields",
    "depends": ["base","sale"],
    "application": True,
    "sequence": "1",
    'data': [
        'security/ir.model.access.csv',
        'views/product_brand_view.xml',
        'views/sale_order_view.xml',
        'views/contact_view.xml',


    ],
    'license': 'LGPL-3',

}