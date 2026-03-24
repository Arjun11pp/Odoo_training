# -*- coding: utf-8 -*-
from odoo import api, fields, models

class EmployeeLoanLine(models.Model):
    _name = 'employee.loan.line'
    _description = 'Employee Loan Line'
    _rec_name = 'loan_id'

    loan_id = fields.Many2one('employee.loan',string='Loan ID')
    date = fields.Datetime(string='Date of Loan')
    amount = fields.Float(string='Amount')
    paid = fields.Boolean(string='Paid')
