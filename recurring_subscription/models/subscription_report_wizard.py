# -*- coding: utf-8 -*-

from odoo import fields,models

class SubscriptionReportWizard(models.TransientModel):
    _name = "subscription.report.wizard"

    subscription_id = fields.Many2many('recurring.subscription',string="Subscription")
    duration=fields.Selection([('daily',"daily"),('weekly','Weekly'),('monthly','Monthly'),('yearly','Yearly')],string="Duration")

    def action_subscription_report_button(self):
        data={
            'subscription_id':self.subscription_id.ids,
            'duration':self.duration,
        }
        return self.env.ref('recurring_subscription.action_report_subscription').report_action(None,data)