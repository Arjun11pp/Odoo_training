# -*- coding: utf-8 -*-
{
    "name": "CRM Dashboard",
    "version": "1.0",
    "description": """CRM Dashboard""",
    "sequence": "2",
    "depends": ["base", "sale", ],
    'data': [
        'security/crm_security.xml',
        'views/sales_team_view.xml',
        'views/crm_custom_menu_view.xml',
    ],
    "application": True,
    "installable": True,
'assets': {
   'web.assets_backend': [
       'crm_dashboard/static/src/js/dashboard.js',
       'crm_dashboard/static/src/js/manager_dashboard.js',
       'crm_dashboard/static/src/xml/dashboard_for_manager.xml',
# 'crm_dashboard/static/src/xml/dashboard_for_manager.xml',
       'crm_dashboard/static/src/xml/dashboard.xml',

       'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.js'
   ],
},
    'author': 'Cybrosys',
    'license': 'LGPL-3',
}
