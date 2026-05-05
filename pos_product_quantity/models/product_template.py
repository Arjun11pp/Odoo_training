# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template'

    selected_stock_location_id = fields.Many2one('stock.location')
    qty_location = fields.Float(string='Quantity')

    @api.model
    def _load_pos_data_fields(self, config_id):
        """ load data into POS """
        data = super()._load_pos_data_fields(config_id)
        data .append('qty_location')
        print('data111', data)
        return data