# -*- coding: utf-8 -*-

{
    'name': "CRM Attachment ",
    'version': '19.0.1',
    'category': 'CRM',
    'sequence': 2,
    'summary': " Attach files or links inside a crm lead ",
    'description': "Attach files or links inside a crm lead ",
    'application' : True,
    'installable': True,
    'depends': ['crm'],
    'data': [
       'views/crm_lead_view.xml',
    ],

    'author': 'Cybrosys.',
    'license': 'LGPL-3',

}
