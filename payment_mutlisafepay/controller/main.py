# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.payment.logging import get_payment_logger
import hmac
import pprint
from werkzeug.exceptions import Forbidden


_logger = get_payment_logger(__name__)

class MultisafepayController(http.Controller):
    _return_url = '/payment/multisafepay/return'
    _webhook_url = '/payment/multisafepay/webhook'

    @http.route(_return_url, type='http', auth='public', methods=['POST'], csrf=False, save_session=False
    )
    def multisafepay_return_from_checkout(self, **data):

        _logger.info("Handling redirection from multisafepay with data:\n%s", pprint.pformat(data))

        tx_sudo = request.env['payment.transaction'].sudo()._search_by_reference('multisafepay', data)
        if tx_sudo:
            # self._verify_signature(data, tx_sudo)
            tx_sudo._process('multisafepay', data)
        return request.redirect('/payment/status')

    @http.route(_webhook_url, type='http', auth='public', methods=['POST'], csrf=False)
    def multisafepay_webhook(self, **data):

        _logger.info("Notification received from APS with data:\n%s", pprint.pformat(data))
        tx_sudo = request.env['payment.transaction'].sudo()._search_by_reference('multisafepay', data)
        if tx_sudo:
            # self._verify_signature(data, tx_sudo)
            tx_sudo._process('multisafepay', data)
        return ''  # Acknowledge the notification.

    # @staticmethod
    # def _verify_signature(payment_data, tx_sudo):
    #
    #     received_signature = payment_data.get('signature')
    #     if not received_signature:
    #         _logger.warning("Received payment data with missing signature.")
    #         raise Forbidden()
    #
    #     # Compare the received signature with the expected signature computed from the data.
    #     expected_signature = tx_sudo.provider_id._aps_calculate_signature(
    #         payment_data, incoming=True
    #     )
    #     if not hmac.compare_digest(received_signature, expected_signature):
    #         _logger.warning("Received payment data with invalid signature.")
    #         raise Forbidden()
