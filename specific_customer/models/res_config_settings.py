# -*- coding: utf-8 -*-

from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _name = 'res.config.settings'

    sale_order_tag_id=fields.One2many('res.partner','category_id')