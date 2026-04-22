# -*- coding: utf-8 -*-

{
    'name': "Bank Book Report ",
    'version': '19.0.1',
    'category': 'Accounting',
    'sequence': 2,
    'summary': " Generates Bank book report in both Excel and PDF formats ",
    'description': " ",
    'application' : True,
    'installable': True,
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_move_menu_view.xml',
        'report/bank_report.xml',
        'report/bank_report_action.xml',
    ],
'assets': {

        'web.assets_backend': [
            'bank_book_report/static/src/js/action_manager.js',
        ],
    'author': 'Cybrosys.',
    'license': 'LGPL-3',
}
}