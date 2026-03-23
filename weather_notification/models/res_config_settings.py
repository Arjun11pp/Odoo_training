# -*- coding: utf-8 -*-

from odoo import fields, models,api

class ResConfigSettings(models.TransientModel):
    """ Configuration settings for weather notification """

    _inherit = 'res.config.settings'

    weather_api_key=fields.Char(string='API Key')

    @api.model
    def get_values(self):
        """Get the values from settings."""
        res = super(ResConfigSettings, self).get_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()
        weather_api_key = icp_sudo.get_param('res.config.settings.weather_api_key')
        res.update(
            weather_api_key= weather_api_key
        )
        return res

    def set_values(self):
        """Set the values. The new values are stored in the configuration parameters."""
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.weather_api_key',
            self.weather_api_key)
        return res