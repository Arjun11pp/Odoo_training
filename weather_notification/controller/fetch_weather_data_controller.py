# -*- coding: utf-8 -*-
from odoo import http
# from odoo.http import request
import requests


class FetchWeatherDataController(http.Controller):
    @http.route('/request/submit', type='jsonrpc', auth='user')
    def get_weather_data(self):
        print('1234')
        user=self.env.user.partner_id
        latitude=user.partner_latitude
        longitude=user.partner_longitude
        url=f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid=a7b5f91f8b72fb52e428cef7868ff6e5"
        response = requests.get(url)

        data = response.json()
        print(data)
        return data
     # https://api.openweathermap.org/data/3.0/onecall?lat=33.44&lon=-94.04&appid={a7b5f91f8b72fb52e428cef7868ff6e5}

