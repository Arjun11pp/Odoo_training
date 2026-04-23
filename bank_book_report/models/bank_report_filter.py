# -*- coding: utf-8 -*-

from odoo import models,api
from datetime import datetime
class BankReportFilter(models.AbstractModel):
    _name = 'report.bank_book_report.report_bank'
    _description = " Bank Report Filter for PDF Report"

    @api.model
    def _get_report_values(self, docids, data):
        """ function for generating reports """
        query = """ SELECT aml.create_date ,aml.move_name,aml.name,aml.debit,aml.credit,aml.balance, res.name AS customer ,aa.name as account,aj.code AS journal FROM account_move_line AS aml 
                    LEFT JOIN account_move am ON aml.move_id = am.id LEFT JOIN res_partner res ON aml.partner_id = res.id
                    LEFT JOIN account_account aa ON aml.account_id = aa.id 
                    LEFT JOIN account_journal aj ON aml.journal_id = aj.id WHERE 1=1 """

        journals= data['journal']
        data['company_name']=self.env.company.name
        data['journal']=self.env['account.journal'].search([('id','=',journals)]).mapped('code')
        data['account_names']=self.env['account.account'].search([('id','=',data['accounts'])]).mapped('name')
        accounts= data['accounts']
        target_moves= data['target_moves']
        sort_by= data['sort_by']
        start_date= data['start_date']
        end_date= data['end_date']
        include_initials= data['include_initials']
        if data['include_initials']:
            lines = self.env['account.move.line'].search([('account_id', 'in', accounts), ('date', '<', start_date)])
            initial_debit = sum(lines.mapped('debit'))
            initial_credit = sum(lines.mapped('credit'))
            data['initial_balance'] = initial_debit - initial_credit
        else:
            data['initial_balance']=0
        if len(accounts)==1:
            query += " AND aml.account_id = %s" % accounts[0]
        elif accounts:
            accounts=tuple(accounts)
            query += " AND aml.account_id IN %s" % (accounts,)
        if start_date != False:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            query += "  AND  aml.create_date >= '%s' " % start_date
        if end_date != False:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            query += "  AND  aml.create_date <= '%s' " % end_date
        if len(journals)==1:
            query += "AND aml.journal_id = %s" % journals[0]
        elif journals:
            journals=tuple(journals)
            query += "AND aml.journal_id IN %s" % (journals,)
        if target_moves =='posted':
            query += "AND aml.parent_state = '%s'" % target_moves
        if sort_by == 'date':
            query += " ORDER BY aml.create_date DESC"
        elif sort_by == 'journal':
            query += " ORDER BY aj.code DESC"
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        for doc in report:
            doc['create_date']=doc['create_date'].date()
        debit_total=sum(d['debit'] for d in report)
        credit_total=sum(d['credit'] for d in report)
        balance_total=sum(d['balance'] for d in report)
        data['debit_total']=debit_total
        data['credit_total']=credit_total
        data['balance_total']=balance_total
        data = [data]
        return {
            'doc_ids': docids,
            'doc_model': 'account.move.line',
            'docs': report,
            'data': data,
            'include_initial': include_initials,
        }