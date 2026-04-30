# -*- coding: utf-8 -*-

from odoo import fields, models,api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = "Inherits res config Settings"

    require_attachment = fields.Boolean(default=False,string="Require Attachment on Purchase Order Confirmation")

    @api.model
    def get_values(self):
        """Get the values from settings."""
        res = super(ResConfigSettings, self).get_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()
        require_attachment = icp_sudo.get_param('res.config.settings.require_attachment')
        res.update(
            require_attachment=require_attachment)
        return res

    def set_values(self):
        """Set the values. The new values are stored in the configuration parameters."""
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.require_attachment', self.require_attachment)
        return res