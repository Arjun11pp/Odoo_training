# -*- coding: utf-8 -*-

from odoo import models,fields,api

class PosSession(models.Model):
    _inherit = 'pos.session'

    discount_limit_amount = fields.Float('Discount Amount')

    @api.model
    def _load_pos_data_fields(self, config_id):
        res = super()._load_pos_data_fields(config_id)
        icp_sudo = self.env['ir.config_parameter'].sudo()
        discount_limit_toggle = icp_sudo.get_param('res.config.settings.discount_limit_toggle')
        discount_limit = icp_sudo.get_param('res.config.settings.discount_limit')
        self.write({'discount_limit_amount': discount_limit})
        res += ['discount_limit_amount']
        return res
