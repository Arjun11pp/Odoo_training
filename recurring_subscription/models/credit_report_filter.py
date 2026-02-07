# -*- coding: utf-8 -*-

from odoo import models,api

class CreditReportFilter(models.AbstractModel):
    _name = 'report.recurring_subscription.report_subscription_credit'

    @api.model
    def _get_report_values(self,docids,data):
        query = """ SELECT cr.id ,sub.name as SubscriptionName,res.name AS customer,cr.credit_amount, cr.state, bill.applied_credit as applied FROM recurring_subscription_credit AS cr  
        LEFT JOIN recurring_subscription AS sub ON cr.recurring_subscription_id = sub.id LEFT JOIN res_partner AS res ON sub.customer_id = res.id 
        LEFT JOIN billing_schedule AS bill ON bill.selected_credit_id = cr.id WHERE 1=1 """

        cr=data['credit_id']
        if len(cr) == 1:
            credit_id=int(cr[0])
            query += " AND cr.id = %s" % credit_id
        elif cr:
            credits_id = str(tuple(cr))
            query += " AND cr.id IN %s" % credits_id
        if data['state'] == 'pending':
            state_id = str(data['state'])
            query += " AND cr.state = '%s'" % state_id
        elif data['state'] == 'confirmed':
            state_id = str(data['state'])
            query += " AND cr.state = '%s'" % state_id
        elif data['state'] == 'approved':
            state_id = str(data['state'])
            query += " AND cr.state = '%s'" % state_id
        elif data['state'] == 'rejected':
            state_id = str(data['state'])
            query += " AND cr.state = '%s'" % state_id

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()

        return {
            'doc_ids': docids,
            'doc_model': 'recurring.subscription.credit',
            'docs': report,
        }


