# -*- coding: utf-8 -*-

from odoo import fields, models,api
from odoo.exceptions import ValidationError
from odoo import Command

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    purchase_order_id = fields.Integer("Purchase Order ID")
    restricted_count = fields.Integer("Restricted Count",related='partner_id.restricted_count')
    restricted=fields.Boolean("Restricted",related='partner_id.restricted')

    @api.onchange('order_line')
    def onchange_order_line(self):
        if self.restricted and len(self.order_line)> self.restricted_count:
            raise ValidationError('NO of order lines are greater than restricted count')

    def action_add(self):
        # self.env['purchase.order.line'].create({
        #     'order_id': self.id,
        #     'product_id': 20,
        #     'price_subtotal': 100
        # })
        self.order_line  = [
                Command.create({'product_id': 20,
             'price_subtotal': 100
                })]

