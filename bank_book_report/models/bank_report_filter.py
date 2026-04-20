# -*- coding: utf-8 -*-

from odoo import fields,models,api

class BankReportFilter(models.AbstractModel):
    _name = 'report.bank_book_report.report_bank'

    @api.model
    def _get_report_values(self, docids, data):
        print('docs',data)
        query = """ SELECT am.sequence_prefix ,am.name,res.name AS customer  FROM account_move AS am  LEFT JOIN res_partner res ON am.partner_id = res.id """
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        print('report',report)
        return {
            'doc_ids': docids,
            'doc_model': 'account.move',
            'docs': report,
            'data': data,
        }