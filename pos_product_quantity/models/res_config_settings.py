# -*- coding: utf-8 -*-

from odoo import fields, models,api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = "Inherits res config Settings"

    product_location_toggle = fields.Boolean(string='Choose location ')
    pos_config_location_id = fields.Many2one('pos.session')
    product_location = fields.Many2one('stock.location',string='Choose Location',readonly=False,store=True,config_parameter='stock.pos_config_location_id')

    @api.model
    def get_values(self):
        """Get the values from settings"""
        res = super(ResConfigSettings, self).get_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()
        product_location_toggle = icp_sudo.get_param('res.config.settings.product_location_toggle')
        product_location = icp_sudo.get_param('res.config.settings.product_location')
        res.update(
            product_location_toggle=product_location_toggle,
            product_location=product_location,
        )
        print('res', res)
        return res

    def set_values(self):
        """Set the values. The new values are stored in the configuration parameters."""
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.product_location_toggle', self.product_location_toggle)
        prints=self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.product_location', self.product_location)
        print('pp', prints,res)
        return res

    @api.model
    def _load_pos_data_fields(self, config_id):
        """ load data fields into POS """
        data = super()._load_pos_data_fields(config_id)
        data += ['product_location']
        return data