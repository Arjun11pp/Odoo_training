# -*- coding: utf-8 -*-
# from custom.payment_mutlisafepay.controller.main import MultisafepayController
from odoo import api, fields, models,_
from odoo.addons.payment import utils as payment_utils

from werkzeug.urls import url_decode, url_parse
from odoo.exceptions import ValidationError
from odoo.tools import urls
from odoo.addons.payment.const import CURRENCY_MINOR_UNITS
from odoo.addons.payment.logging import get_payment_logger
_logger = get_payment_logger(__name__)

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    # def _get_specific_rendering_values(self, processing_values):
    #     """ Override of payment to return Mollie-specific rendering values.
    #     Note: self.ensure_one() from `_get_processing_values`
    #     :param dict processing_values: The generic and specific processing values of the transaction
    #     :return: The dict of provider-specific rendering values
    #     :rtype: dict
    #     """
    #     print("1111",self.provider_code)
    #     if self.provider_code != 'multisafepay':
    #         print("2222")
    #         redirect_url="/payment/multisafepay/redirect"
    #         return {'api_url': redirect_url}
    #     return super()._get_specific_rendering_values(processing_values)

    def _get_specific_rendering_values(self, processing_values):
        """ Override of payment to return Mollie-specific rendering values.

        Note: self.ensure_one() from `_get_processing_values`

        :param dict processing_values: The generic and specific processing values of the transaction
        :return: The dict of provider-specific rendering values
        :rtype: dict
        """
        if self.provider_code != 'multisafepay':
            return super()._get_specific_rendering_values(processing_values)

        payload = self._multisafepay_prepare_payment_request_payload()
        # print('payload',payload)
        try:
            # api_key=self.multisafepay_api_key
            # print('api_key',api_key)
            payment_data = self._send_api_request('POST', '/json/orders?api_key=1c058829cc7994a94bdbabbd614c03b73b3562fc', json=payload)
        except ValidationError as error:
            self._set_error(str(error))
            return {}

        # The provider reference is set now to allow fetching the payment status after redirection
        self.provider_reference = payment_data.get('id')
        print("1111", payment_data)
        # Extract the checkout URL from the payment data and add it with its query parameters to the
        # rendering values. Passing the query parameters separately is necessary to prevent them
        # from being stripped off when redirecting the user to the checkout URL, which can happen
        # when only one payment method is enabled on Mollie and query parameters are provided.
        # checkout_url = payment_data['_links']['checkout']['href']
        # parsed_url = url_parse(checkout_url)
        # url_params = url_decode(parsed_url.query)
        # print('urls', url_params,payment_data,checkout_url)
        # return {'api_url': checkout_url, 'url_params': url_params}
    def _multisafepay_prepare_payment_request_payload(self):
        """ Create the payload for the payment request based on the transaction values.

        :return: The request payload
        :rtype: dict
        """
        # user_lang = self.env.context.get('lang')
        base_url = self.provider_id.get_base_url()
        _return_url = '/payment/multisafepay/redirect'
        _webhook_url = '/payment/multisafepay/webhook'
        redirect_url = urls.urljoin(base_url, _return_url)
        webhook_url = urls.urljoin(base_url, _webhook_url)
        print('self',self)

        return {
            'type': 'redirect',
            'order_id': self.id,

            'amount': self.amount,
            'currency': "USD",
            "payment_options": {
                "notification_method": "POST",
                # "notification_url": "https://www.example.com/webhooks/payment",
                # 'return_url': urls.urljoin(base_url, MultisafepayController._return_url),
                # "cancel_url": "https://www.example.com/order/failed",
                "close_window": False
            },
            "customer": {
                "locale": "en_US",
                "disable_send_email": False
            },
            "checkout_options": {"validate_cart": False},
            "days_active": 30,
            "seconds_active": 2592000,
            # 'api_url': self.provider_id._multisafepay_get_api_url(),
            'description': self.reference,

            # 'locale': user_lang if user_lang in const.SUPPORTED_LOCALES else 'en_US',
            # 'method': [const.PAYMENT_METHODS_MAPPING.get(
            #     self.payment_method_code, self.payment_method_code
            # )],
            'return_url': f'{redirect_url}?ref={self.reference}',
            'notification_url': f'{webhook_url}?ref={self.reference}',
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

        amount_data = payment_data.get('amount', {})
        amount = amount_data.get('value')
        currency_code = amount_data.get('currency')
        return {
            'amount': float(amount),
            'currency_code': currency_code,
        }

    def _apply_updates(self, payment_data):
        """Override of `payment` to update the transaction based on the payment data."""
        if self.provider_code != 'multisafepay':
            return super()._apply_updates(payment_data)
        print("transactions")
        # Update the payment method.
        # payment_method_type = payment_data.get('method', '')
        # if payment_method_type == 'creditcard':
        #     payment_method_type = payment_data.get('details', {}).get('cardLabel', '').lower()
        # payment_method = self.env['payment.method']._get_from_code(
        #     payment_method_type, mapping=const.PAYMENT_METHODS_MAPPING
        # )
        # self.payment_method_id = payment_method or self.payment_method_id

        # Update the payment state.
        payment_status = payment_data.get('status')
        if payment_status in ('pending', 'open'):
            self._set_pending()
        elif payment_status == 'authorized':
            self._set_authorized()
        elif payment_status == 'paid':
            self._set_done()
        elif payment_status in ['expired', 'canceled', 'failed']:
            self._set_canceled(_("Cancelled payment with status: %s", payment_status))
        else:
            _logger.info(
                "Received data with invalid payment status (%s) for transaction %s.",
                payment_status, self.reference
            )
            self._set_error(_("Received data with invalid payment status: %s.", payment_status))

        # url = "https://testapi.multisafepay.com/v1/json/orders"
        # payload = {
        #     "type": "redirect",
        #     "order_id": "my-order-id-1",
        #     "currency": "EUR",
        #     "amount": 37485,
        #     "description": "Test Order Description",
        #     "payment_options": {
        #         "notification_method": "POST",
        #         "notification_url": "https://www.example.com/webhooks/payment",
        #         "redirect_url": "https://www.example.com/order/success",
        #         "cancel_url": "https://www.example.com/order/failed",
        #         "close_window": False
        #     },
        #     "customer": {
        #         "locale": "en_US",
        #         "disable_send_email": False
        #     },
        #     "checkout_options": {"validate_cart": False},
        #     "days_active": 30,
        #     "seconds_active": 2592000
        # }
        # headers = {
        #     "accept": "application/json",
        #     "content-type": "application/json"
        # }
        # response = requests.post(url, json=payload, headers=headers)
        # print(response.text)

        # def _get_specific_rendering_values(self, processing_values):
        #     """ Override of `payment` to return specific processing values.
        #     Note: self.ensure_one() from `_get_processing_values`
        #     :param dict processing_values: The generic processing values of the transaction.
        #     :return: The dict of provider-specific processing values.
        #     :rtype: dict
        #     """
        #     if self.provider_code != 'multisafepay':
        #         return super()._get_specific_rendering_values(processing_values)
        #
        #     base_url = self.provider_id.get_base_url()
        #     print('self',self)
        #     rendering_values = {
        #
        #         'type':'redirect',
        #         'order_id': self.id,
        #         'currency':'USD',
        #         'amount': self.amount,
        #         "payment_options": {
        #             "notification_method": "POST",
        #             "notification_url": "https://www.example.com/webhooks/payment",
        #             # 'return_url': urls.urljoin(base_url, MultisafepayController._return_url),
        #             "cancel_url": "https://www.example.com/order/failed",
        #             "close_window": False
        #         },
        #         "customer": {
        #             "locale": "en_US",
        #             "disable_send_email": False
        #         },
        #         "checkout_options": {"validate_cart": False},
        #         "days_active": 30,
        #         "seconds_active": 2592000,
        #         'api_url': self.provider_id._multisafepay_get_api_url(),
        #     }
        #     return rendering_values