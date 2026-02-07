# -*- coding: utf-8 -*-
from odoo import models,fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    billing_invoice_id = fields.Many2one(comodel_name='billing.schedule',string='Billing Invoice')