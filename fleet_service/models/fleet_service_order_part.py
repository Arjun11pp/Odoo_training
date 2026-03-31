# -*- coding: utf-8 -*-

from odoo import fields, models, api

class FleetServiceOrderPart(models.Model):
    _name = 'fleet.service.order.part'
    _rec_name = 'product_id'

    order_id = fields.Many2one('fleet.service.order')
    product_id = fields.Many2one('product.product')
    quantity = fields.Float('Quantity')
    unit_price = fields.Float('Unit Price')

    @api.onchange('product_id')
    def onchange_product_id(self):
        price=self.product_id.lst_price
        self.write({'unit_price':price})

