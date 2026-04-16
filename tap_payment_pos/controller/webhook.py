# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.tools import verify_hash_signed
import json
import logging
_logger = logging.getLogger(__name__)


class PosTap(http.Controller):
    @http.route('/pos_tap/webhook', methods=['POST'], auth='public', type='jsonrpc', csrf=False)
    def tap_webhook(self,**kwargs):
        raw_data = request.httprequest.data
        data = json.loads(raw_data)
        payment_id=data.get('id')
        payload = request.httprequest.args.get('payload')
        payment_method_sudo = request.env["pos.payment.method"].sudo()
        decoded_payload = verify_hash_signed(payment_method_sudo.env, "pos_tap", payload)
        if not decoded_payload:
            _logger.warning("Invalid payload received in Tap webhook, ignoring")
            return "OK"
        payment_method_id = decoded_payload["payment_method_id"]
        pos_session_id = decoded_payload["pos_session_id"]
        payment_method_sudo = payment_method_sudo.browse(payment_method_id).exists()
        if not payment_method_sudo:
            _logger.warning("No payment method found matching Tap webhook, ignoring")
            return "OK"
        pos_session_sudo = request.env["pos.session"].sudo().browse(pos_session_id).exists()
        if not pos_session_sudo:
            _logger.warning("No POS session found matching Tap webhook, ignoring")
            return "OK"
        payment_info = payment_method_sudo._tap_get_payment(payment_id)
        message = {
            'session_id': int(pos_session_id),
            'payment_id': payment_id,
            'status': payment_info["status"],
        }
        if message['status'] == "PAID":
            message |= {
                'object': payment_info.get("object"),
            }
        elif message['status'] in ['expired', 'failed', 'canceled']:
            message |= {
                'status_reason': payment_info.get("statusReason"),
            }
        pos_session_sudo.config_id._notify('TAP_PAYMENT_STATUS', message)
        return "OK"
