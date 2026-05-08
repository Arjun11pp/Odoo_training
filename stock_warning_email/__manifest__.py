# -*- coding: utf-8 -*-

{
    'name': "Stock warning email",
    'version': '19.0.1',
     'category': 'Supply Chain/Inventory',
    'sequence': 2,
    'summary': " Send a stock warning email to the inventory manager.",
    'description': "Send a stock warning email to the inventory manager. ",
    'application' : True,
    'installable': True,
    'depends': ['stock'],
    'data': [
        'data/email_template.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/inventory_threshold_list.xml',
        'views/stock_warehouse_views.xml',
    ],
    'author': 'Cybrosys',
    'license': 'LGPL-3',

}