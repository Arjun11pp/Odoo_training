# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.addons.payment import utils as payment_utils
from odoo.tools import urls


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _compute_reference(self, provider_code, prefix=None, separator='-', **kwargs):

        if provider_code == 'multisafepay':
            prefix = payment_utils.singularize_reference_prefix()

        return super()._compute_reference(provider_code, prefix=prefix, separator=separator, **kwargs)

    def _get_specific_rendering_values(self, processing_values):
        """ Override of `payment` to return APS-specific processing values.

        Note: self.ensure_one() from `_get_processing_values`

        :param dict processing_values: The generic processing values of the transaction.
        :return: The dict of provider-specific processing values.
        :rtype: dict
        """
        if self.provider_code != 'multisafepay':
            return super()._get_specific_rendering_values(processing_values)

        converted_amount = payment_utils.to_minor_currency_units(self.amount, self.currency_id)
        # base_url = self.provider_id.get_base_url()
        # payment_option = aps_utils.get_payment_option(self.payment_method_id.code)
        rendering_values = {
            # 'command': 'PURCHASE',
            # 'access_code': self.provider_id.aps_access_code,
            # 'merchant_identifier': self.provider_id.aps_merchant_identifier,
            # 'merchant_reference': self.reference,
            'amount': str(converted_amount),
            'currency': self.currency_id.name,
            # 'language': self.partner_lang[:2],
            # 'customer_email': self.partner_id.email_normalized,
            # 'return_url': urls.urljoin(base_url, APSController._return_url),
        }
        # if payment_option:  # Not included if the payment method is 'card'.
        #     rendering_values['payment_option'] = payment_option
        rendering_values.update({
            'signature': self.provider_id._aps_calculate_signature(
                rendering_values, incoming=False
            ),
            'api_url': self.provider_id._aps_get_api_url(),
        })
        return rendering_values