# -*- coding: utf-8 -*-

{
    'name': "Purchase Order Attachment",
    'version': '19.0.1',
     'category': 'Supply Chain/Inventory',
    'sequence': 2,
    'summary': " Mandatory Attachment Before Confirming Purchase Order",
    'description': "Mandatory Attachment Before Confirming Purchase Order ",
    'application' : True,
    'installable': True,
    'depends': ['purchase'],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'author': 'Cybrosys',
    'license': 'LGPL-3',

}