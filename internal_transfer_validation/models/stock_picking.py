# -*- coding: utf-8 -*-

from odoo import fields, models

class StockPicking(models.Model):
    """ Inherits from StockPicking """
    _inherit = "stock.picking"

    state = fields.Selection(selection_add=[
        ('approval', "Approval "),
        ('done',)
    ])

    def action_approve_transfer(self):
        """ Approve transfer button action changes state to approval """
        self.write({'state': 'approval'})
