# -*- coding: utf-8 -*-

from odoo import models, fields, api

class RecurringSubscriptionCredit(models.Model):
    _name = 'recurring.subscription.credit'
    _description = 'Recurring Subscription Credit'
    _rec_name = 'recurring_subscription_id'
    _inherit = 'mail.thread'

    recurring_subscription_id=fields.Many2one('recurring.subscription',string='Name',required=True)
    partner_id=fields.Many2one('res.partner',string='Customer',related="recurring_subscription_id.customer_id")
    company_id = fields.Many2one('res.company',  copy=False,
                                 string="Company", default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id', default=lambda self: self.env.user.company_id.currency_id.id)
    credit_amount=fields.Monetary(string='Credit Amount',default=1)
    state=fields.Selection(selection=[('pending','Pending'),('confirmed','Confirmed'),('approved','Fully Approved'),('rejected','rejected')],string='State',default='pending',tracking=True)
    period_date=fields.Date(string='Period Date',required=True)
    establishment_id=fields.Char(string='Establishment',related="recurring_subscription_id.establishment")
    due_date=fields.Date(related="recurring_subscription_id.due_date", string="Due Date")
    active = fields.Boolean(string='Active', default=True)
    credit_image = fields.Image(string='Image', related='recurring_subscription_id.image')


    _check_credit_amount = models.Constraint(
        'CHECK(credit_amount > 0 )',
        'The Expected price should be positive.')

    @api.onchange('credit_amount')
    def _onchange_credit_amount(self):
        for record in self:
            if record.credit_amount <= 0   or record.credit_amount > record.recurring_subscription_id.recurring_amount :
                record.write({'recurring_subscription_id' : ''})