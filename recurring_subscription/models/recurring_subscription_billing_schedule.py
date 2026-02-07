# -*- coding: utf-8 -*-
import datetime

from odoo import fields, models, api
from odoo import Command

class RecurringSubscriptionBillingSchedule(models.Model):
    _name = 'billing.schedule'
    _description = 'Billing Schedule'
    _inherit = 'mail.thread'

    name=fields.Char(string='Name',required=True)
    simulation=fields.Boolean(string='Simulate',default=True)
    period=fields.Date(string='Period')
    restrict_customer=fields.Many2many('res.partner',string='Restrict Customer')
    active=fields.Boolean(string='Active',default=True)
    recurring_subscription_ids=fields.Many2many(string='Recurring Subscription',comodel_name='recurring.subscription',store=True ,required=True)
    company_id = fields.Many2one('res.company', copy=False,
                                 string="Company", default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',default=lambda self: self.env.user.company_id.currency_id.id)
    total_credit=fields.Monetary(string='Total Credit amount' ,default= 0)
    credit_ids=fields.Many2many(comodel_name='recurring.subscription.credit', compute='_compute_credit_list')
    count=fields.Integer(compute='_compute_credit_count' , string="Subscription Count")
    invoice_ids=fields.Many2many('account.move', string='Invoice')
    applied_credit=fields.Monetary(string='Applied Credit')
    selected_credit_id=fields.Many2one(string='Selected Credit',comodel_name='recurring.subscription.credit')

    @api.depends('recurring_subscription_ids')
    def _compute_credit_count(self):
        for rec in self:
            rec.update({'count' : len(rec.mapped('recurring_subscription_ids')) })

    def action_get_recurring_subscriptions(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Subscriptions',
            'view_mode': 'list,form',
            'res_model': 'recurring.subscription',
            'domain': [('billing_ids', '=', self.ids)],
            'context': "{'create': False}"
        }

    def action_get_invoice(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'view_mode': 'list,form',
            'res_model': 'account.move',
            'domain': [('billing_invoice_id', '=', self.id)],
            'context': "{'create': False}"
        }

    @api.depends('recurring_subscription_ids','recurring_subscription_ids.credit_ids')
    def _compute_credit_list(self):
        for rec in self:
            rec.update({'credit_ids': [Command.link(lists) for lists in rec.recurring_subscription_ids.mapped('credit_ids').filtered(lambda c: c.state == 'approved').ids ]
                    })

    @api.onchange('recurring_subscription_ids')
    def onchange_credit_amount(self):
        for rec in self:
            for record in rec.recurring_subscription_ids:
                credit_list = record.mapped('credit_ids')
                amount=credit_list.mapped('credit_amount')
                rec.update({'total_credit':sum(amount)})

    def action_create_billing_invoice(self):
        for record in self.recurring_subscription_ids:
            partner=record.customer_id
            credit_list=self.env['recurring.subscription.credit'].search([('recurring_subscription_id','=',record.id),('state','=','approved')])
            for credit in credit_list:
                if credit:
                    if credit.credit_amount == record.recurring_amount :
                        selected_credit=credit.id
                        final=credit.credit_amount
                    elif credit.credit_amount <= record.recurring_amount :
                        cdate=min(credit.mapped('create_date'))
                        selected_credit=self.env['recurring.subscription.credit'].search([('create_date','=',cdate)]).id
                        final=(self.env['recurring.subscription.credit'].search([('create_date','=',cdate)])).credit_amount
            total=record.recurring_amount
            final_total=-final

            product=record.product_id.id
            credit_product=self.env.ref('recurring_subscription.product_id1')
            self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': partner.id,
                'billing_invoice_id' : self.id,
                    'line_ids': [Command.create({'product_id': product ,'price_unit' : total }) ,
                                 Command.create({'product_id': credit_product.id ,'price_unit' : final_total }) ,
                                ]})
            self.update({'active': False})
            self.update({'applied_credit': final})
            self.update({'selected_credit_id': selected_credit})

    def action_automatic_invoice(self):
        for rec in (self.search([('active','=',True)])):
            due=(rec.recurring_subscription_ids. filtered(lambda s: s.due_date and s.due_date < datetime.date.today()).mapped('due_date'))
            if due:
                for record in rec.recurring_subscription_ids:
                    if record.due_date < datetime.date.today():
                        partner = record.customer_id
                        credit_list = record.env['recurring.subscription.credit'].search(
                            [('recurring_subscription_id', '=', record.id),('state','=','approved')])
                        for credit in credit_list:
                            if credit.credit_amount == record.recurring_amount:
                                final_credit = credit.credit_amount
                                selected_credit = credit.id
                            elif credit.credit_amount <= record.recurring_amount:
                                cdate = min(credit.mapped('create_date'))
                                selected_credit=record.env['recurring.subscription.credit'].search([('create_date', '=', cdate)])
                                final_credit = (record.env['recurring.subscription.credit'].search([('create_date', '=', cdate)])).credit_amount
                        total = record.recurring_amount
                        final_total = -final_credit
                        product = record.product_id.id
                        # prod_id = self.env['product.product'].create({'name': "subscription "+ record.name +",  " + str(record.create_date.date()) })
                        credit_product = self.env.ref('recurring_subscription.product_id1')
                        record.env['account.move'].create({
                            'move_type': 'out_invoice',
                            'partner_id': partner.id,
                            'billing_invoice_id': rec.id,
                            'line_ids': [Command.create({'product_id': product, 'price_unit': total}) ,
                                         Command.create({'product_id': credit_product.id, 'price_unit': final_total})
                                         ]})
                        rec.write({'active': False})
                        self.update({'applied_credit': final_credit})
                        self.update({'selected_credit_id': selected_credit})