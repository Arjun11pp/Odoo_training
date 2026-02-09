# -*- coding: utf-8 -*-

from odoo import fields,models

class CreditReportWizard(models.TransientModel):
    _name = "credit.report.wizard"

    credit_id = fields.Many2many('recurring.subscription.credit',string="Subscription credit")
    state=fields.Selection(selection=[('pending','Pending'),('confirmed','Confirmed'),('approved','Fully Approved'),('rejected','rejected')],string='State')

    def action_credit_report_button(self):
        data = {
            'credit_id': self.credit_id.ids,
            'state': self.state,
        }

        return self.env.ref('recurring_subscription.action_report_credit').report_action(None, data)