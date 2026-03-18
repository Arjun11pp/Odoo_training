# -*- coding: utf-8 -*-

from odoo import fields, models,api

class PosConfig(models.Model):
    _inherit = 'pos.config'

    print_limit=fields.Float('Print Limit')
    print_count=fields.Float('Print Count',default=0)

    # @api.model
    # def get_values(self):
    #     """Get the values from settings."""
    #     res = super(PosConfig, self).get_values()
    #     icp_sudo = self.env['ir.config_parameter'].sudo()
    #
    #     print_limit = icp_sudo.get_param('pos.config.print_limit')
    #     res.update(
    #
    #         print_limit=float(print_limit) if print_limit else 0.0,
    #     )
    #     # print('res', res)
    #     return res
    #
    # def set_values(self):
    #     """Set the values. The new values are stored in the configuration parameters."""
    #
    #     res = super(PosConfig, self).set_values()
    #
    #     self.env['ir.config_parameter'].sudo().set_param(
    #         'pos.config.print_limit',
    #         self.price_limit)
    #     print('res', res)
    #     return res

    # @api.model
    # def _load_pos_data_fields(self, config_id):
    #     data = super()._load_pos_data_fields(config_id)
    #
    #     data += ['print_limit']
    #     return data

    @api.model
    def _load_pos_data_read(self,records,config):
        read_records = super()._load_pos_data_read(records,config)
        read_records += ['print_limit']
        read_records += ['print_count']
        return read_records