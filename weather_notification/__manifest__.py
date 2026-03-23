# -*- coding: utf-8 -*-
{
    "name": "Weather Notification",
    "version": "1.0",
    "description": """Wearher Notification """,
    "sequence": "2",
    "depends": ["base"],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'assets': {
   'web.assets_backend': [

       'weather_notification/static/src/js/systray_icon.js',
       'weather_notification/static/src/xml/systray_icon.xml',

   ],
},

    "application": True,
    "installable": True,
    'author': 'Cybrosys',
}