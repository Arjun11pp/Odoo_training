# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo import Command
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    _description = 'Purchase Order'

    split_order_id = fields.Integer(string='Split Order ID')

    def action_get_split_purchase(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Order',
            'view_mode': 'list,form',
            'res_model': 'purchase.order',
            'domain': [('split_order_id', '=', self.id)],
        }

    def button_confirm(self):
        vendor_list = {}
        product_quantity = {}
        product_price = {}
        vendor_select={}
        for stock in self:
            for products in stock.order_line:
                if products.product_id not in product_quantity:
                    product_quantity[products.product_id]=products.product_qty
                else:
                    product_quantity[products.product_id] += products.product_qty
                product_price[products.product_id]=products.price_unit
                for order in products.product_id:
                    if not order.seller_ids:
                        raise ValidationError(_('The product %s has no vendor', order.name))
                    for price in order.seller_ids:
                        vendor_select[price.partner_id]=price.price
                    min_key = min(vendor_select, key=vendor_select.get)
                    vendor_list.setdefault(min_key.id, [])
                    vendor_list[min_key.id].append(order)
            for key,value in vendor_list.items():
                po_id = self.env['purchase.order'].create({
                    "partner_id": key,
                    "split_order_id": self.id,
                })
                for items in value:
                    product_id = items.id
                    product_name = items.name
                    order_line_id = po_id.order_line
                    if product_id not in order_line_id.product_id.ids:

                        po_id.write({
                            "order_line": [
                                Command.create({
                                    'product_id': product_id,
                                    'name': product_name,
                                    'price_unit': product_price[items],
                                    'product_qty': product_quantity[items],
                                }),]})

        return super(PurchaseOrder,self).button_confirm()