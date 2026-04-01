# -*- coding: utf-8 -*-
{
    "name": "fleet service",
    "version": "1.0",
    "description": """fleet service""",
    "sequence": "2",
    "depends": ["base","fleet","hr"],
    'data': [
        'security/ir.model.access.csv',
        'views/fleet_vehicle_view.xml',
        'views/hr_employee_view.xml',
        'data/ir_sequence_data.xml',
        'views/fleet_service_order_views.xml',
        'views/menu_items.xml',
    ],
    "application": True,
    "installable": True,

    'author': 'Cybrosys',

}