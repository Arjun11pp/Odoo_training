# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from dateutil.utils import today
from odoo.tools import hash_sign

class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    def _get_payment_terminal_selection(self):
        return super()._get_payment_terminal_selection() + [("tap", "Tap")]
    tap_payment_provider_id = fields.Many2one("payment.provider", domain=[("code", "=", "tap")])

    @api.constrains('tap_payment_provider_id')
    def _check_tap_payment_provider_id(self):
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
        currency = self.journal_id.currency_id or self.company_id.currency_id
        formatted_amount = f"{amount:.3f}"
        payload = {
            "payment_uuid": payment_uuid,
            "payment_method_id": self.id,
            "pos_session_id": pos_session_id,
        }
        signed_payload = hash_sign(self.sudo().env, "pos_tap", payload, expiration_hours=27)  # Tap webhooks can retry for up to 26 hours
        dt=fields.Datetime.add(today(), days=2)
        millis = int(dt.timestamp() * 1000)
        payment_request = {
            "draft": False,
            "due": millis,
            "expiry": millis,
            "description": "test invoice",
            "mode": "INVOICE",
            "currencies": [currency.name],
            "customer": {
                "first_name": "test123",
                "last_name": "test123",
                "email": "odootestperson@gmail.com",
                "phone": {
                    "country_code": 965,
                    "number": 51234467
                }
            },
            "notifications": {
                "channels": ["SMS", "EMAIL"],
                "dispatch": True
            },
            "charge": {"receipt": {
                "email": True,
                "sms": True
            }},
            "order": {
                "amount": formatted_amount,
                "currency": currency.name,
                "items": [ {
                            "amount": formatted_amount,
                            "description": "test",
                            "name": "pos",
                            "quantity": 1,
                            "currency": currency.name
                            } ],
               },
            "post":{'url': f"{self.get_base_url()}/pos_tap/webhook?payload={signed_payload}"},
            # "redirect": {"url":  f"{self.get_base_url()}/pos/ui/1/receipt/"},
            "retry_for_captured": True,
            "reference": {
                "invoice": self.id,
            },
            "statement_descriptor": "test"
        }
        print('self',self.tap_payment_provider_id)
        return self.tap_payment_provider_id._send_api_request("POST", "/invoices", json=payment_request)

    def tap_cancel_payment(self, payment_id: str):
        self.ensure_one()
        return self.tap_payment_provider_id._send_api_request("DELETE", f"/invoices/{payment_id}")

    def tap_get_payment(self, payment_id: str):
        print('self',self)
        # self.ensure_one()
        print('payment',self.tap_payment_provider_id)
        for data in  self.tap_payment_provider_id._send_api_request("GET", f"/invoices/{payment_id}"):
            print(data)
        return self.tap_payment_provider_id._send_api_request("GET", f"/invoices/{payment_id}")

    # def tap_create_refund(self, original_payment_id: str, amount: float, payment_uuid: str, pos_session_id: int):
    #     print('create refund')
    #     self.ensure_one()
    #     currency = self.journal_id.currency_id or self.company_id.currency_id
    #     payment_request = {
    #         "amount": {
    #             "currency": currency.name,
    #             "value": f"{amount:.{currency.decimal_places}f}"
    #         },
    #         "description": f"pos_session_id={pos_session_id},payment_uuid={payment_uuid}",
    #     }
    #     return self.tap_payment_provider_id._send_api_request("POST", f"/payments/{original_payment_id}/refunds", json=payment_request)