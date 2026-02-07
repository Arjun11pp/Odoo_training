# -*- coding: utf-8 -*-

from odoo import fields, models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    transfer_id=fields.Many2one(comodel_name='material.request',string='Transfer')