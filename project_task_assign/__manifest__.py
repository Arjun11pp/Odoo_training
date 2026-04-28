# -*- coding: utf-8 -*-

{
    'name': "Project Task",
    'version': '19.0.1',
    'category': 'Project',
    'sequence': 2,
    'summary': " Auto-set task assignee based on skill tag ",
    'description': " Auto-set task assignee based on skill tag",
    'application' : True,
    'installable': True,
    'depends': ['base','project' ],
    'data': [
        'views/res_users_view.xml',
        'views/project_task_view.xml',
    ],

    'author': 'Cybrosys',
    'license': 'LGPL-3',

}