# -*- coding: utf-8 -*-
{
    "name": "Sale Order Approval",
    "version": "19.0.1.0.0",
    "sequence": "1",
    "author": "Cybrosys",
    "application": True,
    "depends": ['base', 'mail', 'account', 'sale'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',

        'views/sale_order_view.xml',

    ],
    'license': 'LGPL-3',
}
