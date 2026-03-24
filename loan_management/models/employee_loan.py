# -*- coding: utf-8 -*-

from odoo import api, fields, models,_
from odoo.exceptions import ValidationError


class EmployeeLoan(models.Model):
    _name = 'employee.loan'
    _description = 'Employee Loan'

    name=fields.Char(string='Name', default=lambda self: _('New'),readonly=True)
    employee_id = fields.Many2one('hr.employee')
    loan_amount = fields.Float(string='Loan Amount', required=True)
    installment_count=fields.Float(string='Installment Count', required=True)
    start_date=fields.Datetime(string='Start Date', required=True)
    state = fields.Selection([('draft','Draft'),('approved','Approved'),('ongoing','Ongoing'),('paid','Paid')],String='Status', default='draft')
    loan_line_ids=fields.One2many('employee.loan.line','loan_id',string='Loan Lines')
    installment_amount=fields.Float(string='Installment Amount', default=0)
    total_payable=fields.Float(string='Total Payable', compute='_compute_total_payable')
    loan_line_ids_count=fields.Float(string='Loan Lines Count',compute='_compute_loan_count')

    paid_amount = fields.Float(string='Paid', compute='_compute_paid_amount')
    balance_amount = fields.Float(string='Balance', compute='_compute_balance')

    def _compute_balance(self):
        balance=0
        for record in self.loan_line_ids:
            if record.paid == False:
                balance+=record.amount
        self.write({'balance_amount':balance})

    def _compute_paid_amount(self):
        total = 0
        for record in self.loan_line_ids:
            if record.paid== True:
                total+=record.amount
        print('total',total)
        self.write({'paid_amount':total})

    @api.onchange('loan_amount','installment_count')
    def _installment_amount(self):
        if self.installment_count !=0:
            amount=self.loan_amount/self.installment_count
            self.write({'installment_amount':amount})

    def _compute_total_payable(self):
        for record in self:
            total=record.loan_amount
            record.write({'total_payable':total})

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            if val.get('name', _('New')) == _('New'):
                val['name'] = self.env['ir.sequence'].next_by_code('employee.loan')
        return super().create(vals)

    def action_approve(self):
        print(self.loan_amount)
        if self.loan_amount > 0.0:
            self.state = 'approved'
        else:
            raise ValidationError("Loan amount must be greater than 0")

    def _compute_loan_count(self):
        count = len(self.loan_line_ids)
        self.write({'loan_line_ids_count': count})

    def action_get_loan_details(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'loan details',
            'view_mode': 'list,form',
            'res_model': 'employee.loan.line',
            'domain': [('loan_id', 'in', self.ids)],
            'context': "{'create': False}"
        }

    def action_create_installment(self):
        print('123')
        for record in self:
            count=int(record.installment_count)
            print('count',count)
            for rec in range(count):
                self.env['employee.loan.line'].create({
            'loan_id': self.id,
            'date': self.start_date,
            'amount': self.installment_amount,
        })
        self.write({'state': 'ongoing'})

    def action_pay_installment(self):
        unpaid_installments=self.env['employee.loan.line'].search([('loan_id','=', self.id),('paid','=',False)],limit=1)
        for record in unpaid_installments:
            if record:
                record.write({'paid':True})
                if self.balance_amount ==0:
                    self.write({'state': 'paid'})
        



