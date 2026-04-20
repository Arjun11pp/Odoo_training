# -*- coding: utf-8 -*-

from odoo import api, fields, models
import json
from odoo.tools import date_utils, json_default
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

class AccountMove(models.TransientModel):
    _name = "account.move.report.wizard"
    """ model for bank_book_report wizard """

    target_moves=fields.Selection([('posted','All Posted Entries '),('all','All Entries')],string="Target Entries",required=True)
    sort_by=fields.Selection([('date','Date'),('journal','Journal & Partner')],string="Sort By",required=True)
    include_initials=fields.Boolean(default=False)
    start_date = fields.Date(default=fields.Datetime.today(), string="Start Date")
    end_date = fields.Date(string="End Date")
    # def _get_bank_accounts(self):
    #     print('self',self.env['account.account'].search([('')]))
    accounts=fields.Many2many("account.account", string="Accounts"
                              # default=_get_bank_accounts
                              )
    journal=fields.Many2many("account.journal", string="Journal")


    def action_bank_report_button(self):
        print('pressed')
        data = {
            'target_moves': self.target_moves,
            'sort_by': self.sort_by,
            'include_initials': self.include_initials,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'accounts': self.accounts.ids,
            'journal': self.journal.ids,
        }
        return self.env.ref('bank_book_report.action_report_bank_book').report_action(None, data)

    def action_print_xlsx(self):
        data = {
            'target_moves': self.target_moves,
            'sort_by': self.sort_by,
            'include_initials': self.include_initials,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'accounts': self.accounts.ids,
            'journal': self.journal.ids,
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'account.move.report.wizard',
                     'options': json.dumps(data, default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Bank Report',
                     },
            'report_type': 'xlsx',
        }