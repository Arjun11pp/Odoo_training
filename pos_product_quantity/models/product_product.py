# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ProductProduct(models.Model):
    _inherit = 'product.product'

    # product_location_id = fields.Many2one('stock.location')

    @api.model
    def _load_pos_data_fields(self, config_id):
        data = super()._load_pos_data_fields(config_id)
        # icp_sudo = self.env['ir.config_parameter'].sudo()
        # product_location_toggle = icp_sudo.get_param('res.config.settings.product_location_toggle')
        # product_location_id = icp_sudo.get_param('res.config.settings.product_location_id')
        # self.write({'product_location_id': product_location_id})

        data += ['qty_available', 'type', 'is_storable','stock_quant_ids']
        print('data111',data)
        return data