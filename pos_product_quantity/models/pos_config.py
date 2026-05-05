
# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class PosConfig(models.Model):
    _inherit = 'pos.config'

    product_stock_location_id = fields.Many2one('stock.location')

    @api.model
    def _load_pos_data_read(self, records, config):
        print('records', records)
        read_records = super()._load_pos_data_read(records, config)
        icp_sudo = self.env['ir.config_parameter'].sudo()
        product_location_toggle = icp_sudo.get_param('res.config.settings.product_location_toggle')
        product_location_id = icp_sudo.get_param('res.config.settings.product_location_id')
        self.write({'product_stock_location_id': product_location_id})
        read_records[0]['product_stock_location_id'] = product_location_id
        return read_records