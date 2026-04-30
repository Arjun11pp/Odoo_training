# -*- coding: utf-8 -*-

from odoo import models,fields,api

class PosSession(models.Model):
    _inherit = 'pos.session'

    product_location_id = fields.Many2one('stock.location')

    @api.model
    def _load_pos_data_fields(self, config_id):
        res = super()._load_pos_data_fields(config_id)
        icp_sudo = self.env['ir.config_parameter'].sudo()
        product_location_id = icp_sudo.get_param('res.config.settings.product_location_id')
        self.write({'product_location_id': product_location_id})
        res += ['product_location_id']
        print('res1234', res)
        return res
