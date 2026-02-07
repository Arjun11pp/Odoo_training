# -*- coding: utf-8 -*-
from odoo import models,fields

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    brand_ids = fields.Many2one(related="product_id.brand_id",string="Brand")