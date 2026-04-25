# -*- coding: utf-8 -*-

from odoo import  models

class StockPicking(models.Model):
    _inherit = "stock.picking"
    _description = 'Inherits Stock Picking model'

    def button_validate(self):
        """ super button validate function """
        res =super(StockPicking,self).button_validate()
        print('ids',self.product_id)
        for products in self.product_id:
            products._compute_quantities()
        return res