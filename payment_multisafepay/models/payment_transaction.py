# -*- coding: utf-8 -*-

from odoo import api,  models,_
from odoo.addons.payment import utils as payment_utils

from werkzeug.urls import url_decode, url_parse
from odoo.exceptions import ValidationError
from odoo.tools import urls
from odoo.addons.payment.const import CURRENCY_MINOR_UNITS
from odoo.addons.payment.logging import get_payment_logger
_logger = get_payment_logger(__name__)

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """ Override of payment to return multisafepay-specific rendering values.
        Note: self.ensure_one() from `_get_processing_values`
        :param dict processing_values: The generic and specific processing values of the transaction
        :return: The dict of provider-specific rendering values
        :rtype: dict
        """
        if self.provider_code != 'multisafepay':
            return super()._get_specific_rendering_values(processing_values)
        payload = self._multisafepay_prepare_payment_request_payload()
        try:
            payment_data = self._send_api_request('POST', '/json/orders', json=payload)
        except ValidationError as error:
            self._set_error(str(error))
            return {}
        order_data= payment_data.get('data',payment_data)
        self.provider_reference = payment_data.get('order_id',self.reference)
        payment_url=order_data.get('payment_url','')
        return {'api_url': payment_url, 'url_params': {}}

    def _multisafepay_prepare_payment_request_payload(self):
        """ Create the payload for the payment request based on the transaction values.
        :return: The request payload
        :rtype: dict
        """
        base_url = self.provider_id.get_base_url()
        _return_url = '/payment/multisafepay/return'
        _webhook_url = '/payment/multisafepay/webhook'
        redirect_url = urls.urljoin(base_url, _return_url)
        webhook_url = urls.urljoin(base_url, _webhook_url)

        currency_code = self.currency_id.name
        final_amount=int(round(self.amount*100))

        return {
            'type': 'redirect',
            'order_id': self.reference,
            'amount': final_amount,
            'currency': currency_code,
            "payment_options": {
                "notification_method": "POST",
                "close_window": False,
                'redirect_url': f'{redirect_url}?ref={self.reference}',
                'notification_url': f'{webhook_url}?ref={self.reference}'
            },
            "customer": {
                "locale": "en_US",
                "disable_send_email": False
            },
            "checkout_options": {"validate_cart": False},
            "days_active": 30,
            "seconds_active": 2592000,
            'description': self.reference,
        }

    @api.model
    def _extract_reference(self, provider_code, payment_data):
        """Override of `payment` to extract the reference from the payment data."""
        if provider_code != 'multisafepay':
            return super()._extract_reference(provider_code, payment_data)
        return payment_data.get('ref')

    def _extract_amount_data(self, payment_data):
        """Override of `payment` to extract the amount and currency from the payment data."""
        if self.provider_code != 'multisafepay':
            return super()._extract_amount_data(payment_data)
        amount_data = payment_data.get('data', {})
        amount = amount_data.get('amount')/100
        currency_code = amount_data.get('currency')
        return {
            'amount': float(amount),
            'currency_code': currency_code,
        }

    def _apply_updates(self, payment_data):
        """Override of `payment` to update the transaction based on the payment data."""
        if self.provider_code != 'multisafepay':
            return super()._apply_updates(payment_data)
        payment_status = payment_data.get('success')
        if payment_status == False:

            self._set_canceled(_("Cancelled payment with status: %s", payment_status))
        elif payment_status == True:
            self._set_done()
        else:
            _logger.info(
                "Received data with invalid payment status (%s) for transaction %s.",
                payment_status, self.reference
            )
            self._set_error(_("Received data with invalid payment status: %s.", payment_status))

