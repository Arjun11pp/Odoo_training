# -*- coding: utf-8 -*-

{
    'name': "Auot hide products",
    'version': '19.0.1',
    'category': 'CRM',
    'sequence': 2,
    'summary': " Auto Hide Out of Stock Products ",
    'description': "Auto Hide Out of Stock Products ",
    'application' : True,
    'installable': True,
    'depends': ['base'],
    'data': [
        'views/product_template_views.xml',
    ],

    'author': 'Cybrosys',
    'license': 'LGPL-3',

}
