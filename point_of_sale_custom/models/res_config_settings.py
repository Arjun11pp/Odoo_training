# -*- coding: utf-8 -*-

from odoo import api, fields, models
class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'
    discount_limit_toggle = fields.Boolean(string='Limit  discounts ')
    pos_config_limit_id=fields.Many2one('pos.session')
    discount_limit = fields.Float(string='Discount Limit',related='pos_config_limit_id.discount_limit_amount',readonly=False,store=True)

    @api.model
    def get_values(self):
        """Get the values from settings."""
        res = super(ResConfigSettings, self).get_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()
        discount_limit_toggle = icp_sudo.get_param('res.config.settings.discount_limit_toggle')
        discount_limit = icp_sudo.get_param('res.config.settings.discount_limit')
        res.update(
            discount_limit_toggle=discount_limit_toggle,
            discount_limit=float(discount_limit) if discount_limit else 0.0 ,
        )
        # print('res', res)
        return res
    def set_values(self):
        """Set the values. The new values are stored in the configuration parameters."""
        if not self.discount_limit_toggle:
            self.discount_limit = 0.0
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.discount_limit_toggle', self.discount_limit_toggle)
        self.env['ir.config_parameter'].sudo().set_param(
            'res.config.settings.discount_limit',
            self.discount_limit)
        # print('res', res)
        return res

    # @api.model
    # def _load_pos_data_fields(self, config_id):
    #     data = super()._load_pos_data_fields(config_id)
    #     data += ['discount_limit']
    #     return data