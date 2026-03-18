# -*- coding: utf-8 -*-
from odoo import models,fields

class ProductBrand(models.Model):
    _name='product.brand'
    _rec_name = "brand"

    brand = fields.Char(string="Brand")