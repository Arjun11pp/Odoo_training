# -*- coding: utf-8 -*-

from odoo import http
import requests

class FetchWeatherDataController(http.Controller):
    """ Controller for fetching weather data """
    @http.route('/request/submit', type='jsonrpc', auth='user')
    def get_weather_data(self):
        user=self.env.user.partner_id
        latitude=user.partner_latitude
        longitude=user.partner_longitude
        icp_sudo = self.env['ir.config_parameter'].sudo()
        api_key=icp_sudo.get_param('res.config.settings.weather_api_key')
        if not api_key:
            return False
        else:
            url=f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={api_key}"
            response = requests.get(url)
            data = response.json()
            return data

     # https://api.openweathermap.org/data/3.0/onecall?lat=33.44&lon=-94.04&appid={a7b5f91f8b72fb52e428cef7868ff6e5} a7b5f91f8b72fb52e428cef7868ff6e5
