# -*- coding: utf-8 -*-
from email.policy import default

from odoo import api, fields, models

class InventoryWarning(models.Model):
    _name = 'inventory.warning'
    _description = 'Inventory Warning'

    product_id = fields.Many2one('product.product',string='Select Product')
    quantity = fields.Float(string='Quantity')
    warehouse_id = fields.Many2one('stock.warehouse',string='Warehouse')
    # manager_id=fields.Many2one('res.users',string='Manager',
    # compute='_default_res_users')

    # def _default_res_users(self):
    #     users_obj = self.env['res.users']
    #     users = []
    #     for user in users_obj.search([]):
    #         if user.has_group("stock_warning_email.group_inventory_manager"):
    #             users.append(user.id)
    #             print('user', user)
    #     self.write({'manager_id': users[0]})
    #     return users