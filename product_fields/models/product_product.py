# -*- coding: utf-8 -*-
from odoo import models,fields,api

class ProductProduct(models.Model):
    _inherit = "product.product"

    average_cost = fields.Float(string="Average Cost",compute="_compute_average_of_price",readonly=True)

    def _compute_average_of_price(self):
        quantity =  sum(self.env['purchase.order.line'].search([('product_id', '=', self.id)]).filtered(lambda line: line.state== 'purchase').mapped('product_qty'))

        total_price = sum(self.env['purchase.order.line'].search([('product_id', '=', self.id)]).filtered(lambda line: line.state== 'purchase').mapped('price_subtotal'))
        if quantity>0 and total_price>0:
            avg = total_price / quantity
            self.write({'average_cost' :  avg })
        else:
            self.write({'average_cost' :  0})