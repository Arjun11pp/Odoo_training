# -*- coding: utf-8 -*-

{
    'name': "Purchae order splitting ",
    'version': '19.0.1',
    'category': 'CRM',
    'sequence': 2,
    'summary': "  Purchase Order Splitting Based on Vendor Pricing ",
    'description': " Purchase Order Splitting Based on Vendor Pricing",
    'application' : True,
    'installable': True,
    'depends': ['base','product', 'purchase', ],
    'data': [
        'views/purchase_order_view.xml',
    ],

    'author': 'Cybrosys',
    'license': 'LGPL-3',

}