# -*- coding: utf-8 -*-
from odoo import fields,models,api

class BankReportFilter(models.AbstractModel):
    _name = 'report.bank_book_report.report_bank'

    @api.model
    def _get_report_values(self, docids, data):
        # print('docs',data)
        query = """ SELECT aml.create_date ,aml.move_name,aml.name,aml.debit,aml.credit,aml.balance, res.name AS customer ,aa.name as account,aj.code AS journal FROM account_move_line AS aml 
                    LEFT JOIN account_move am ON aml.move_id = am.id LEFT JOIN res_partner res ON aml.partner_id = res.id LEFT JOIN account_account aa ON aml.account_id = aa.id 
                    LEFT JOIN account_journal aj ON aml.journal_id = aj.id WHERE 1=1 """

        journals= data['journal']
        company_name=self.env.company
        data['company_name']=company_name.name

        journal_names=self.env['account.journal'].search([('id','=',journals)]).mapped('code')
        data['journal']=journal_names
        print('journals',type(journal_names),type(data))
        accounts= data['accounts']
        print('accounts',type(accounts))
        target_moves= data['target_moves']
        sort_by= data['sort_by']
        start_date= data['start_date']
        end_date= data['end_date']
        if len(accounts)==1:
            query += " AND aml.account_id = %s" % accounts[0]
        elif accounts:
            accounts=tuple(accounts)
            query += " AND aml.account_id IN %s" % (accounts,)
        if start_date and end_date:
            query += "  AND  aml.create_date >= '%s' AND aml.create_date <= '%s' " % (start_date, end_date)
        # print('123',journals)
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
        print('report',report)
        for doc in report:
            doc['create_date']=doc['create_date'].date()

        data=[data]

        return {
            'doc_ids': docids,
            'doc_model': 'account.move.line',
            'docs': report,
            'data': data,
        }