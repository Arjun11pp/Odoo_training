# -*- coding: utf-8 -*-

from odoo import fields, models

class AccountPayment(models.Model):
    _inherit = "account.payment"
    _description = "Inherits Active Invoice"

    def action_post(self):
        """ function to super action_post funvtion """
        for move in self.invoice_ids:
            if move.payment_state != 'paid':
                amount=move.final_invoice_amount
                payment_register = self.env['account.payment.register'].with_context(active_model='account.move',
                    active_ids=move.ids).create({
                    'payment_date': fields.Datetime.today(),
                    'journal_id': self.env.ref('account.1_bank').id,
                    'amount': amount,
                })
                payment_register.action_create_payments()
        return super(AccountPayment, self).action_post()