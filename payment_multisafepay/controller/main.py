# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.payment.logging import get_payment_logger
from odoo.exceptions import ValidationError
import pprint


_logger = get_payment_logger(__name__)

class MultisafepayController(http.Controller):
    _return_url = '/payment/multisafepay/redirect'
    _webhook_url = '/payment/multisafepay/webhook'

    @http.route(_return_url, type='http', auth='public', methods=['POST'], csrf=False, save_session=False)
    def multisafepay_return_from_checkout(self, **data):
        """Process the payment data sent by Mollie after redirection from checkout.

        The route is flagged with `save_session=False` to prevent Odoo from assigning a new session
        to the user if they are redirected to this route with a POST request. Indeed, as the session
        cookie is created without a `SameSite` attribute, some browsers that don't implement the
        recommended default `SameSite=Lax` behavior will not include the cookie in the redirection
        request from the payment provider to Odoo. As the redirection to the '/payment/status' page
        will satisfy any specification of the `SameSite` attribute, the session of the user will be
        retrieved and with it the transaction which will be immediately post-processed.

        :param dict data: The payment data (only `id`) and the transaction reference (`ref`)
                          embedded in the return URL.
        """
        print("checkout")
        _logger.info("handling redirection from Mollie with data:\n%s", pprint.pformat(data))
        self._verify_and_process(data)
        return request.redirect('/payment/status')

    @http.route(_webhook_url, type='http', auth='public', methods=['POST'], csrf=False)
    def mmultisafepay_webhook(self, **data):
        """Process the payment data sent by Mollie to the webhook.

        :param dict data: The payment data (only `id`) and the transaction reference (`ref`)
                          embedded in the return URL
        :return: An empty string to acknowledge the notification
        :rtype: str
        """
        print("webhook")
        _logger.info("notification received from multisafepay with data:\n%s", pprint.pformat(data))
        self._verify_and_process(data)
        return ''  # Acknowledge the notification

    @staticmethod
    def _verify_and_process(data):
        """Verify and process the payment data sent by Mollie.

        :param dict data: The payment data.
        :return: None
        """
        print("verify")
        tx_sudo = request.env['payment.transaction'].sudo()._search_by_reference('multisafepay', data)
        if not tx_sudo:
            return

        try:
            verified_data = tx_sudo._send_api_request(
                'GET', f'/payments/{tx_sudo.provider_reference}'
            )
        except ValidationError:
            _logger.error("Unable to process the payment data")
        else:
            tx_sudo._process('multisafepay', verified_data)