# -*- coding: utf-8 -*-

{
    'name': "Payment Provider: Tap ",
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 350,
    'summary': "Payment Provider: Tap ",
    'description': " ",
    'depends': ['payment'],
    'data': [
        'views/payment_tap_templates.xml',
        'views/payment_provider_views.xml',
        'data/payment_provider_data.xml',
        'data/payment_method_data.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}