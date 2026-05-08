# -*- coding: utf-8 -*-

from odoo import  fields, models

class InventoryWarning(models.Model):
    """Inventory warning model created to set threshold limit to products ,
     So it sends warning email to the warehouse manager """
    _name = 'inventory.warning'
    _description = 'Inventory Warning'

    product_id = fields.Many2one('product.product',string='Select Product')
    quantity = fields.Float(string='Quantity')
    warehouse_id = fields.Many2one('stock.warehouse',string='Warehouse')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company.id)
