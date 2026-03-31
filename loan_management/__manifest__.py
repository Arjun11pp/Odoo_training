# -*- coding: utf-8 -*-
{
    "name": "Loan Management",
    "version": "1.0",
    "description": """Loan management app""",
    "sequence": "2",
    "depends": ["base","sale_management","purchase" ,"hr"],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/loan_management_view.xml',
        'views/loan_management_line_view.xml',
        'views/menu_item.xml',
        'views/hr_employee_view.xml',
    ],
    "application": True,
    "installable": True,

    'author': 'Cybrosys',

}