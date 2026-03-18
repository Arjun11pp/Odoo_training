# -*- coding: utf-8 -*-

from odoo import  models

class SaleOrder(models.Model):
    """Inherited sale.order and overriding action_confirm function and change the opportunity stage related to the sales team to the stage defined in crm.team model"""
    _inherit = "sale.order"

    def action_confirm(self):
        """overridies action_confirm function  and change the opportunity stage related to the sales team to the stage defined in crm.team model"""
        team=self.team_id.lead_state_id
        opportunity=self.opportunity_id
        if opportunity:
            self.env['crm.lead'].search([('id','=',opportunity.id)]).write({'stage_id':team.id})
        result = super(SaleOrder, self).action_confirm()
        return result