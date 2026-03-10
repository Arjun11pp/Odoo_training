# -*- coding: utf-8 -*-

from odoo import api,fields,models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_owner_id=fields.Many2one('res.partner',string="Owner")

    @api.model
    def _load_pos_data_fields(self, config_id):
        data = super()._load_pos_data_fields(config_id)

        data += ['product_owner_id']
        return data