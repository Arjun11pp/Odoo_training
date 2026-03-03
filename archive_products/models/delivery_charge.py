    # -*- coding: utf-8 -*-

from odoo import models, fields

class DeliveryCharge(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        product = self.env.ref('archive_products.delivery_product')
        if self.amount_untaxed < 1500:
            self.env['sale.order.line'].create({'order_id': self.id,'product_id': product.id, 'price_unit' : 99})
        result=super(DeliveryCharge,self).action_confirm()
        return result
