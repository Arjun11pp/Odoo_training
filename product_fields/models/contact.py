# -*- coding: utf-8 -*-

from odoo import models,fields

class SaleOrder(models.Model):
    _inherit = "res.partner"

    prime_customer = fields.Boolean(string="Is Prime Customer")