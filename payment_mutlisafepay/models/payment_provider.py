# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.addons.payment_aps import const
import hashlib

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code=fields.Selection(selection_add=[('multisafepay', 'Multi Safe Payment Provider')],ondelete={'multisafepay': 'set default'})
    multisafepay_api_key=fields.Char(string='API Key', copy=False)

    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes. """
        self.ensure_one()
        if self.code != 'multisafepay':
            return super()._get_default_payment_method_codes()
        return const.DEFAULT_PAYMENT_METHOD_CODES

    def _multisafepay_get_api_url(self):
        if self.state == 'enabled':
            return "https://testapi.multisafepay.com/v1/json/orders?api_key="