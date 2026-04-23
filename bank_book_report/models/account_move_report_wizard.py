# -*- coding: utf-8 -*-

from odoo import  fields, models
import json
import io
from datetime import datetime
from odoo.tools import  json_default
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

class AccountMove(models.TransientModel):
    _name = "account.move.report.wizard"
    _description = " Bank Book Report Wizard for generating reports "
    """ model for bank_book_report wizard """

    target_moves=fields.Selection([('posted','All Posted Entries '),('all','All Entries')],string="Target Entries",required=True)
    sort_by=fields.Selection([('date','Date'),('journal','Journal & Partner')],string="Sort By",required=True)
    include_initials=fields.Boolean(default=False,string="Include Initial Balance")
    start_date = fields.Date( string="Start Date",)
    end_date = fields.Date(string="End Date")
    account_ids=fields.Many2many("account.account", string="Accounts")
    journal_ids=fields.Many2many("account.journal", string="Journal")

    def action_bank_report_button(self):
        """ function for bank_book_report wizard """
        data = {
            'target_moves': self.target_moves,
            'sort_by': self.sort_by,
            'include_initials': self.include_initials,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'accounts': self.account_ids.ids,
            'journal': self.journal_ids.ids,
        }
        return self.env.ref('bank_book_report.action_report_bank_book').report_action(None, data)

    def action_print_xlsx(self):
        """ function for bank_book_report wizard xlsx """
        data = {
            'target_moves': self.target_moves,
            'sort_by': self.sort_by,
            'include_initials': self.include_initials,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'accounts': self.account_ids.ids,
            'journal': self.journal_ids.ids,
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

    def get_bank_xlsx_report(self, data, response):
        """ function for bank_book_report wizard XLSX template """
        query = """ SELECT aml.create_date, aml.move_name, aml.name, aml.debit, aml.credit, aml.balance, res.name AS customer, aa.name  as account, aj.code  AS journal 
                    FROM account_move_line AS aml LEFT JOIN account_move am ON aml.move_id = am.id LEFT JOIN res_partner res ON aml.partner_id = res.id 
                    LEFT JOIN account_account aa ON aml.account_id = aa.id LEFT JOIN account_journal aj ON aml.journal_id = aj.id WHERE 1 = 1 """

        journals = data['journal']
        data['company_name']=self.env.company.name
        journal_names = self.env['account.journal'].search([('id', '=', journals)]).mapped('code')
        accounts = data['accounts']
        account_names = self.env['account.account'].search([('id', '=',accounts)]).mapped('name')
        data['account_names'] = account_names
        target_moves = data['target_moves']
        sort_by = data['sort_by']
        start_date = data['start_date']
        end_date = data['end_date']
        if data['include_initials']:
            lines = self.env['account.move.line'].search([('account_id', 'in', accounts), ('date', '<', start_date)])
            initial_debit = sum(lines.mapped('debit'))
            initial_credit = sum(lines.mapped('credit'))
            data['initial_balance'] = initial_debit - initial_credit

        if len(accounts) == 1:
            query += " AND aml.account_id = %s" % accounts[0]
        elif accounts:
            accounts = tuple(accounts)
            query += " AND aml.account_id IN %s" % (accounts,)
        if start_date != False:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            query += "  AND  aml.create_date >= '%s' " % start_date
        if end_date != False:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            query += "  AND  aml.create_date <= '%s' " % end_date
        if len(journals) == 1:
            query += "AND aml.journal_id = %s" % journals[0]
        elif journals:
            journals = tuple(journals)
            query += "AND aml.journal_id IN %s" % (journals,)

        if target_moves == 'posted':
            query += "AND aml.parent_state = '%s'" % target_moves
        if sort_by == 'date':
            query += " ORDER BY aml.create_date DESC"
        elif sort_by == 'journal':
            query += " ORDER BY aj.code DESC"
        self.env.cr.execute(query)
        docs = self.env.cr.dictfetchall()
        for doc in docs:
            doc['create_date']=doc['create_date'].date()
        debit_total = sum(d['debit'] for d in docs)
        credit_total = sum(d['credit'] for d in docs)
        balance_total = sum(d['balance'] for d in docs)
        data['debit_total'] = debit_total
        data['credit_total'] = credit_total
        data['balance_total'] = balance_total
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('docs')

        sheet.set_column(1, 1, 15)
        sheet.set_column(2, 2, 15)
        sheet.set_column(3, 3, 15)
        sheet.set_column(4, 4, 20)
        sheet.set_column(5, 5, 30)
        sheet.set_column(6, 6, 15)
        sheet.set_column(7, 7, 15)
        sheet.set_column(8, 8, 15)
        border = workbook.add_format({'border': 1, 'align': 'left','text_wrap': True})
        company = workbook.add_format({'border': 1, 'align': 'left','text_wrap': True,'font_size': 9})
        date_format=workbook.add_format({ 'num_format': 'yyyy-mm-dd','border': 1, 'align': 'left'})
        title = workbook.add_format({'align': 'left', 'bold': True, 'valign': 'top','border':1})

        head = workbook.add_format({'bold': True, 'font_size': 30, 'align': 'center', 'valign': 'vcenter','bg_color': '#dddddd'})
        sheet.write(3, 1, 'Report Date', title)
        sheet.write(3, 2, fields.Date.today(), date_format)
        sheet.write(3, 7, 'Company',border)
        sheet.write(3, 8, data['company_name'],company)
        sheet.merge_range('B5:I8', 'Bank Report', head)

        if data['journal']:
            sheet.write(10, 1,'Journals  :' , title)
            formatted_names = ", ".join(journal_names)
            sheet.write(10, 2, formatted_names)
        if data['account_names']:
            formatted_account_names = ", ".join(account_names)
        sheet.write(12, 1,'Sorted by' , title)
        sheet.write(13, 1, data['sort_by'].capitalize() )
        sheet.write(12, 3, 'Target Moves', title)
        sheet.write(13, 3, data['target_moves'].capitalize() )
        if data['include_initials'] !=False :
            sheet.write(12, 5, 'Initial balance', title)
            sheet.write(13, 5, data['initial_balance'],border )
        if data['start_date'] !=False :
            sheet.write(12, 6, 'Start Date', title)
            sheet.write(13, 6, data['start_date'])
        if  data['end_date'] != False:
            sheet.write(12, 8, 'End date', title)
            sheet.write(13, 8, data['end_date'])

        sheet.merge_range('B18:B19', 'Date', title)
        sheet.merge_range('C18:C19', 'JRNL', title)
        sheet.merge_range('D18:D19', 'Partner', title)
        sheet.merge_range('E18:E19', 'Move', title)
        sheet.merge_range('F18:F19', 'Entry label', title)
        sheet.merge_range('G18:G19', 'Debit', title)
        sheet.merge_range('H18:H19', 'Credit', title)
        sheet.merge_range('I18:I19', 'Balance', title)
        sheet.merge_range('B20:F20', formatted_account_names, title)
        sheet.write(19, 6, data['debit_total'], border)
        sheet.write(19, 7, data['credit_total'], border)
        sheet.write(19, 8, data['balance_total'], border)
        row = 20
        col = 1
        for doc in docs:
            sheet.write(row, col, doc['create_date'], date_format)
            col += 1
            sheet.write(row, col, doc['journal'], border)
            col += 1
            sheet.write(row, col, doc['customer'], border)
            col += 1
            sheet.write(row, col, doc['move_name'], border)
            col += 1
            sheet.write(row, col, doc['name'], border)
            col += 1
            sheet.write(row, col, doc['debit'], border)
            col += 1
            sheet.write(row, col, doc['credit'], border)
            col += 1
            sheet.write(row, col, doc['balance'], border)
            col = 1
            row += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()