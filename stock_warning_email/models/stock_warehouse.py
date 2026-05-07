# -*- coding: utf-8 -*-

from odoo import fields, models, api

class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"
    _description = "Stock Warehouse"

    manager_id=fields.Many2one('res.users',string="Manager")