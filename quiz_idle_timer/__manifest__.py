# -*- coding: utf-8 -*-
{
    "name": "Quiz idle timer",
    "version": "1.0",
    "description": """Idle timer inside quiz""",
    "sequence": "1",
    "depends": ["base","survey"],
    "data":[
        'views/survey_page_view.xml',
        'views/survey_survey_view.xml',
    ],
    "application": True,
    "installable": True,
    'assets': {
        'web.assets_frontend': [
            'quiz_idle_timer/static/src/js/idle_timer.js',
        ],
        'survey.survey_assets': [
            'quiz_idle_timer/static/src/js/timer_reload.js'
        ],
    },
    'author': 'Cybrosys',

}