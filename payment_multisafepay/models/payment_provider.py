# -*- coding: utf-8 -*-

# from custom.payment_mutlisafepay import const
from odoo import api, fields, models
from odoo.tools import urls

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code=fields.Selection(selection_add=[('multisafepay', 'Multi Safe Payment Provider')],ondelete={'multisafepay': 'set default'})
    multisafepay_api_key=fields.Char(string='API Key', copy=False,required=True)


    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes. """
        print('Payment Method Codes',self)
        self.ensure_one()
        if self.code != 'multisafepay':
            return super()._get_default_payment_method_codes()
        return 'card'

    # def _multisafepay_get_api_url(self):
    #     if self.state == 'enabled':
    #         return "https://testapi.multisafepay.com/v1/json/orders?api_key="

        # === REQUEST HELPERS === #

    def _build_request_url(self, endpoint, **kwargs):
        """Override of `payment` to build the request URL."""
        if self.code != 'multisafepay':
            return super()._build_request_url(endpoint, **kwargs)
        return urls.urljoin('https://testapi.multisafepay.com/v1/', endpoint.strip('/'))

    def _build_request_headers(self, *args, **kwargs):
        """Override of `payment` to build the request headers."""
        if self.code != 'multisafepay':
            return super()._build_request_headers(*args, **kwargs)

        # odoo_version = service.common.exp_version()['server_version']
        # module_version = self.env.ref('base.module_payment_mollie').installed_version
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json',

        }

    def _parse_response_error(self, response):
        """Override of `payment` to parse the error message."""
        if self.code != 'multisafepay':
            return super()._parse_response_error(response)

        return response.json().get('detail', '')