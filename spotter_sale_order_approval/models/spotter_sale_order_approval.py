# -*- coding: utf-8 -*-

from odoo import api, fields, models

class SpotterSaleOrderApproval(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(selection_add=[
        ('user1', "User 1"),
        ('user2', "User 2"),
        ('sent',)
    ])

    def action_approve1(self):
        self.write({'state': 'user1'})


    def action_approve2(self):
        self.write({'state': 'user2'})

    def action_quotation_send(self):

        result=super(SpotterSaleOrderApproval,self).action_quotation_send()
        self.write({'state': 'sent'})
        return result