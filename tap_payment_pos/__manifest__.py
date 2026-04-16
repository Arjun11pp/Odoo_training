# -*- coding: utf-8 -*-

{
    'name': 'POS Tap',
    'version': '1.0',
    'category': 'Sales/Point of Sale',
    'sequence': 6,
    'summary': 'Integrate your POS with a Tap payment terminal',
    'depends': ['point_of_sale', 'tap_payment'],
    'installable': True,
    'data': [
        'views/pos_payment_method_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'tap_payment_pos/static/src/**/*',
            # "tap_payment_pos/static/src/xml/pos_send_button.xml" ,
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
