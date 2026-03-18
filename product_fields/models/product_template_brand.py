# -*- coding: utf-8 -*-
from odoo import models,fields,api

class ProductTemplateBrand(models.Model):
    _inherit = "product.template"

    brand_id = fields.Many2one(comodel_name='product.brand',string="Brand")
    product_master_type=fields.Selection([('single','Single product'),('branded','Branded Product')])


    @api.onchange('product_master_type')
    def onchange_master_type(self):
        if self.product_master_type == 'single':
            self.write({'brand_id': ''})

