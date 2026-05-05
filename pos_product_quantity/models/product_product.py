# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ProductProduct(models.Model):
    _inherit = 'product.product'
    _description = 'Product Product'

    product_stock_location = fields.Float(compute='_compute_stock_location_id')
    selected_stock_location_id = fields.Many2one('stock.location')

    def _compute_stock_location_id(self):
        """ function to compute stock location and quantity """
        for product in self:
            location=product.selected_stock_location_id
            if not location:
                product.write({'product_stock_location':0})
                continue
            print('name',location.name,product.name)
            quantity=self.env['stock.quant'].search([('location_id','=',location.id),('product_id','=',product.id)])
            print('quantity',quantity)
            total=0
            for q in quantity:
                total += q.quantity
            print('total',total)
            product.write({'product_stock_location':total})
            product.product_tmpl_id.qty_location=total


    @api.model
    def _load_pos_data_fields(self, config_id):
        """ load data fields into POS"""
        data = super()._load_pos_data_fields(config_id)
        data += ['qty_available','stock_quant_ids','product_stock_location']
        return data