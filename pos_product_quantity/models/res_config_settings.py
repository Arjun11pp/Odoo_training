# -*- coding: utf-8 -*-

from odoo import fields, models,api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = "Inherits res config Settings"

    product_location_toggle = fields.Boolean(string='Choose location ',config_parameter='pos_product_quantity.product_location_toggle')
    pos_config_location_id = fields.Many2one('pos.session')
    product_location_id = fields.Many2one('stock.location',string='Choose Location',readonly=False,config_parameter='pos_product_quantity.product_location_id',related='pos_config_location_id.product_location_id',store=True)
    # pos_config_location_id = fields.Many2one('pos.session')
    # product_location_id = fields.Many2one('stock.location',string='Choose Location',readonly=False,config_parameter='pos_product_quantity.product_location_id',related='pos_config_location_id.product_location_id',store=True)


    @api.model
    def _load_pos_data_fields(self, config_id):
        """ load data fields into POS """
        data = super()._load_pos_data_fields(config_id)
        data += ['product_location_id']
        print('data1', data)
        return data