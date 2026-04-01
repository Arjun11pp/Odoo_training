# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResPartner(models.Model):
    """Inherits from res_partner model"""
    _inherit = "res.partner"

    most_product_sold = fields.Many2one('product.product',string="Most Product Sold")
    total_sold_quantity = fields.Float(string="Total Sold Quantity",compute="_compute_total_sold_quantity")
    minimum_sale_price = fields.Float(string="Minimum Sold Price",compute="_compute_min_sale_price")
    maximum_sale_price = fields.Float(string="Maximum Sold Price",compute="_compute_max_sale_price")

    def _compute_most_product_sold(self):
        saleorders=self.sale_order_ids
        products={}
        quantity={}
        for order in saleorders.order_line:
            products[order.id]=order.product_id.name
            quantity[order.id]=order.product_uom_qty
            
        print('products',products)
        print('quantity',quantity)
        # self.write({'most_product_sold':products})
        print(saleorders)

    def _compute_total_sold_quantity(self):
        quantity=0
        saleorders = self.sale_order_ids
        for order in saleorders.order_line:
            quantity+=order.product_uom_qty
        self.write({'total_sold_quantity':quantity})

    def _compute_min_sale_price(self):
        total_amount=list()
        saleorders = self.sale_order_ids
        for order in saleorders:
            total_amount.append(order.amount_total)
        mini=min(total_amount)
        print('12',mini)
        self.write({'minimum_sale_price':mini})

    def _compute_max_sale_price(self):
        total_amount = list()
        saleorders = self.sale_order_ids
        for order in saleorders:
            total_amount.append(order.amount_total)
        maximum = max(total_amount)
        self.write({'maximum_sale_price':maximum})