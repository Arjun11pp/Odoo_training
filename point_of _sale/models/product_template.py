# -*- coding: utf-8 -*-

from odoo import api,fields,models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_owner=fields.Many2one('res.partner',string="Owner")