# -*- coding: utf-8 -*-

from odoo import fields, models

class StockWarehouse(models.Model):
    """ Inherits stock.warehouse model """
    _inherit = "stock.warehouse"
    _description = "Stock Warehouse"

    manager_id=fields.Many2one('res.users',string="Manager")