# -*- coding: utf-8 -*-

from odoo import fields, models, api

class ProductTemplate(models.Model):
    _inherit = "product.template"
    _description = " Inherits Product Template model"

    auto_hide_products = fields.Boolean(default=False,string="Auto hide products on website upon out of stock")