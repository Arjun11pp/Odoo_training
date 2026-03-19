# -*- coding: utf-8 -*-

from odoo import models, fields

class ResUser(models.Model):
    _inherit = 'res.users'


    sale_order_ids=fields.One2many('sale.order','partner_id')