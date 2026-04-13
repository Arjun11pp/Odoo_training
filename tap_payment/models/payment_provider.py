# -*- coding: utf-8 -*-

from odoo import  fields, models

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code=fields.Selection(selection_add=[('tap', 'Multi Safe Payment Provider')],ondelete={'tap': 'set default'})
    tap_api_key=fields.Char(string='API Key', copy=False,required=True)

    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes. """
        self.ensure_one()
        if self.code != 'tap':
            return super()._get_default_payment_method_codes()
        return {'tap'}

    def _build_request_url(self, endpoint, **kwargs):
        """Override of `payment` to build the request URL."""
        if self.code != 'tap':
            return super()._build_request_url(endpoint, **kwargs)
        url= 'https://api.tap.company/v2'
        clean_endpoint=endpoint.strip('/')
        return f'{url}/{clean_endpoint}'

    def _build_request_headers(self, *args, **kwargs):
        """Override of `payment` to build the request headers."""
        if self.code != 'tap':
            return super()._build_request_headers(*args, **kwargs)
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.tap_api_key}',
        }

    def _parse_response_error(self, response):
        """Override of `payment` to parse the error message."""
        if self.code != 'tap':
            return super()._parse_response_error(response)
        return response.json().get('detail', '')