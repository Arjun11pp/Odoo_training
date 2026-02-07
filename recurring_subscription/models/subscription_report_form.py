# -*- coding: utf-8 -*-

from odoo import fields,models,api
from odoo.tools import date_utils


class SubscriptionReportForm(models.AbstractModel):
    _name='report.recurring_subscription.report_subscription'

    @api.model
    def _get_report_values(self, docids, data):
        query = """ SELECT rs.sequence_number , rs.name  ,res.name AS customer,temp.name AS product,rs.recurring_amount,rs.total_credit,rs.state ,rs.terms_and_conditions ,bill.applied_credit as appliedcredit
                                      FROM recurring_subscription AS rs LEFT JOIN res_partner res ON rs.customer_id = res.id LEFT JOIN product_product p ON rs.product_id = p.id
                                       LEFT JOIN product_template temp ON p.product_tmpl_id = temp.id LEFT JOIN billing_schedule_recurring_subscription_rel as bs ON bs.recurring_subscription_id = rs.id LEFT JOIN billing_schedule as bill ON bill.id = bs.billing_schedule_id WHERE 1=1 """


        subscription= data ['subscription_id']
        if len(subscription)==1:
            sub=int(subscription[0])
            query += " AND rs.id = %s" % sub
        elif subscription:
            sub = str(tuple(subscription))
            query += " AND rs.id IN %s" % sub
        if data['duration']== 'daily':
            query += " AND rs.date = '%s' " % ( fields.Date.today())
        elif data['duration']== 'weekly':
            start_date = date_utils.start_of(fields.Date.today(), "week")
            end_date = date_utils.end_of(fields.Date.today(), "week")
            query += " AND rs.date >= '%s' AND rs.date <= '%s' " % ( start_date, end_date)
        elif data['duration']== 'monthly':
            start_date = date_utils.start_of(fields.Date.today(), "month")
            end_date = date_utils.end_of(fields.Date.today(), "month")
            query += "  AND  rs.date >= '%s' AND rs.date <= '%s' " % (start_date, end_date)
        elif data['duration']== 'yearly':
            start_date = date_utils.start_of(fields.Date.today(), "year")
            end_date = date_utils.end_of(fields.Date.today(), "year")
            query += " AND  rs.date >= '%s' AND rs.date <= '%s' " % (start_date, end_date)
        query += " ORDER BY rs.sequence_number"
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        print(report)
        return {
            'doc_ids': docids,
            'doc_model': 'recurring.subscription',
            'docs': report,
        }