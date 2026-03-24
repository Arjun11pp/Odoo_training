# -*- coding: utf-8 -*-

from odoo import fields, models,api

class PosConfig(models.Model):
    _inherit = 'pos.config'

    print_limit=fields.Float('Print Limit')
    print_count=fields.Float('Print Count',default=0)

    # @api.model
    # def _load_pos_data_read(self,records,config):
    #     read_records = super()._load_pos_data_read(records,config)
    #     read_records += ['print_limit']
    #     read_records += ['print_count']
    #     return read_records