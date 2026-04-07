# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
# from odoo.addons.payment_mollie import const

from odoo.tools import hash_sign


class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    # code = fields.Selection(selection_add=[('tap', 'Tap Payment Provider')],
    #                         ondelete={'tap': 'set default'})
    # tap_api_key = fields.Char(string='API Key', copy=False, required=True)

    def _get_payment_terminal_selection(self):
        return super()._get_payment_terminal_selection() + [("tap", "Tap")]


    # tap_terminal_id = fields.Char("Tap Terminal ID", copy=False)
    tap_payment_provider_id = fields.Many2one("payment.provider", domain=[("code", "=", "tap")])

    @api.constrains('tap_payment_provider_id')
    def _check_tap_payment_provider_id(self):
        print('check')
        for payment_method in self:
            if not payment_method.tap_payment_provider_id:
                continue
            if not payment_method.tap_payment_provider_id.tap_api_key:
                raise ValidationError(_(
                    'Please set the Tap API Key field on the %s payment provider.',
                    payment_method.tap_payment_provider_id.name
                ))

    def tap_create_payment(self, amount: float, payment_uuid: str, pos_session_id: int):
        self.ensure_one()
        print('create payment')
        user_lang = self.env.context.get("lang")
        currency = self.journal_id.currency_id or self.company_id.currency_id
        payload = {
            "payment_uuid": payment_uuid,
            "payment_method_id": self.id,
            "pos_session_id": pos_session_id,
        }
        signed_payload = hash_sign(self.sudo().env, "pos_tap", payload, expiration_hours=27)  # Tap webhooks can retry for up to 26 hours
        payment_request = {
            
            # "locale": user_lang if user_lang in const.SUPPORTED_LOCALES else "en_US",
            "due": 1672235072000,
            "expiry": 1672235072000,
            "mode": "INVOICE",
            "customer": {
                "first_name": "test",
                "last_name": "test",
                "email": "test@test.com",
                "phone": {
                    "country_code": 965,
                    "number": 51234567
                }
            },
            "order": {
                "amount": f"{amount:.{currency.decimal_places}f}",
                "currency": currency.name
            },
            "description": f"pos_session_id={pos_session_id},payment_uuid={payment_uuid}",
            # "redirectUrl": f"{self.get_base_url()}",
            "redirect": {'url': f"{self.get_base_url()}"},
            "post": {"url": f"{self.get_base_url()}/pos_tap/webhook?payload={signed_payload}"},
            # "webhookUrl": f"{self.get_base_url()}/pos_tap/webhook?payload={signed_payload}",
            # "method": "pointofsale",

        }
        return self.tap_payment_provider_id._send_api_request("POST", "/payments", json=payment_request)

    def tap_create_refund(self, original_payment_id: str, amount: float, payment_uuid: str, pos_session_id: int):
        print('create refund')
        self.ensure_one()

        currency = self.journal_id.currency_id or self.company_id.currency_id
        payment_request = {
            "amount": {
                "currency": currency.name,
                "value": f"{amount:.{currency.decimal_places}f}"
            },
            "description": f"pos_session_id={pos_session_id},payment_uuid={payment_uuid}",
        }
        return self.tap_payment_provider_id._send_api_request("POST", f"/payments/{original_payment_id}/refunds", json=payment_request)

    def tap_cancel_payment(self, payment_id: str):
        self.ensure_one()
        return self.tap_payment_provider_id._send_api_request("DELETE", f"/payments/{payment_id}")

    def _tap_get_payment(self, payment_id: str):
        print('get payment')
        self.ensure_one()
        return self.tap_payment_provider_id._send_api_request("GET", f"/payments/{payment_id}")