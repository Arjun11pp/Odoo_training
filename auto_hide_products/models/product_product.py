# -*- coding: utf-8 -*-

from odoo import fields, models, api

class ProductProduct(models.Model):
    _inherit = 'product.product'
    _description = 'Product Template'

    auto_hide_products = fields.Boolean(default=False, string="Auto hide products on website upon out of stock")

    def _compute_quantities(self):
        print('_compute_quantities')
        result=super(ProductProduct,self)._compute_quantities()
        for rec in self:
            if rec.qty_available <= 0 and rec.auto_hide_products:
                if rec.is_published:
                    rec.write({'is_published':False})
        return result