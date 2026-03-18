# -*- coding: utf-8 -*-

import re
from dateutil.utils import today
from odoo import models, fields, api , _
from odoo.exceptions import ValidationError


class RecurringSubscription(models.Model):
    _name = "recurring.subscription"
    _description = "Recurring Subscription"
    _inherit =  'mail.thread'

    sequence_number = fields.Char(string="Reference Number", default=lambda self: _('New'), readonly=True, copy=False,tracking=True)
    name = fields.Char(required=True,string="Name")
    establishment=fields.Char( string="Establishment ID",required=True  )
    date=fields.Date(string="date",default=fields.Date.today())
    due_date=fields.Date(default=fields.Date.add(today(),days=15), string="Due Date",store=True)
    next_billing_date=fields.Date(string="Next Billing Date")
    is_lead=fields.Boolean(string="Is Lead")
    customer_id=fields.Many2one("res.partner",string="Customer" )
    description=fields.Char(string="Description")
    terms_and_conditions=fields.Html(string="Terms and Conditions")
    product_id=fields.Many2one(comodel_name='product.product',string="Product",required=True)
    company_id = fields.Many2one('res.company',  copy=False,
                                 string="Company", default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id', default=lambda self: self.env.user.company_id.currency_id.id)
    recurring_amount=fields.Monetary(string="Recurring Amount",default=1)
    state=fields.Selection([('draft','Draft'),('confirm','Confirm'),('done','Done'),('cancel','Cancel')],default='draft',string="State",tracking=True)
    credit_ids=fields.One2many(comodel_name='recurring.subscription.credit',inverse_name='recurring_subscription_id', compute="_compute_recurring_subscription_period")
    billing_ids=fields.Many2many('billing.schedule',string='billing schedule',readonly=True)
    active = fields.Boolean(string='Active', default=True)
    total_credit=fields.Monetary(compute='_compute_total_credit', string='Total Credit',store=True)
    image=fields.Binary(string="Image",required=True)

    @api.depends('credit_ids')
    def _compute_total_credit(self):
        total = sum(self.credit_ids.mapped('credit_amount'))
        self.write({'total_credit': total})

    @api.onchange('establishment')
    def search_customer_id(self):
        if self.establishment:
            partner=self.env['res.partner'].search([('establishment_id','=',self.establishment)])
            if partner:
                self.write({ 'customer_id' : partner.id })
            else :
                raise ValidationError("No partner found for this establishment!")

    @api.depends('due_date')
    def _compute_recurring_subscription_period(self):
        for record in self:
             self.update({'credit_ids' : self.env['recurring.subscription.credit'].search([('recurring_subscription_id', '=', self._origin), ('period_date', '<', record.due_date)])})

    _check_credit_amount = models.Constraint(
        'CHECK(recurring_amount == 0 )',
        'The recurring amount should be non zero.')

    @api.constrains('establishment')
    def _check_establishment(self):
        for record in self:
            alphabets = re.findall(r'[a-zA-Z]', record.establishment)
            numbers = re.findall(r'[0-9]', record.establishment)
            special_chars = re.findall(r'[!@#$%^&*()_+={}\[\]:;"\'<,>./?`~\\-]', record.establishment)
            if len(alphabets) <3 or len(numbers) <3 or len(special_chars) <2:
                raise ValidationError("There must be at least 3 alphabets, numbers and 2 special characters!")

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            if val.get('sequence_number', _('New')) == _('New'):
                val['sequence_number'] = self.env['ir.sequence'].next_by_code('recurring.subscription')
        return super().create(vals)

    def action_confirm(self):
        self.write({'state':'confirm'})

    def action_done(self):
        template = self.env.ref('recurring_subscription.subscription_email_template')
        email_values = {'email_from': self.env.user.email}
        template.send_mail(self.id, force_send=True, email_values=email_values)
        self.message_post_with_source(template, subtype_xmlid='recurring_subscription.email_template', )
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state':'cancel'})
        return True