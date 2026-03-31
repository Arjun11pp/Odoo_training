# -*- coding: utf-8 -*-

from odoo import fields, models

class StockPicking(models.Model):
    _inherit = "stock.picking"

    state = fields.Selection(selection_add=[
        ('approval', "Approval "),

        ('done',)
    ])

    # def button_validate(self):
    #     result = super(StockPicking, self).button_validate()
    #     self.write({'state': 'approval'})

    def action_approve_transfer(self):
        print('self',self)
        self.write({'state': 'done'})
