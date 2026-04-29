# -*- coding: utf-8 -*-

from odoo import fields, models

class AccountMove(models.Model):
    _inherit = "account.move"
    _description = "Active Invoice"

    final_invoice_amount = fields.Float(string="Amount")