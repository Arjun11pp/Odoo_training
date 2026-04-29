# -*- coding: utf-8 -*-

{
    'name': "Combined Invoice Payment",
    'version': '19.0.1',
    'category': 'invoice',
    'sequence': 2,
    'summary': " . Combined Invoice Payment ",
    'description': "Combined Invoice Payment ",
    'application' : True,
    'installable': True,
    'depends': ['account'],
    'data': [
        'views/account_payment_view.xml',
    ],
    'author': 'Cybrosys.',
    'license': 'LGPL-3',

}