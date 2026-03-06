# -*- coding: utf-8 -*-

from odoo import api,fields,models

class PosSession(models.Model):
    _inherit = 'pos.session'


    total_discount=fields.Float(string="Total Discount",default=0)



    # def _load_pos_data_fields(self, config_id):
    #     # Call super to get existing fields
    #     res = super()._load_pos_data_fields(config_id)
    #     # Add your custom field to the list
    #     res += ['discount_limit']
    #     return res