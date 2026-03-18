# -*- coding: utf-8 -*-

import io
import json
from odoo.tools import  json_default
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter
from odoo import fields,models

class CreditReportWizard(models.TransientModel):
    _name = "credit.report.wizard"

    subscription_id = fields.Many2many('recurring.subscription',string="Subscription credit")
    state=fields.Selection(selection=[('pending','Pending'),('confirmed','Confirmed'),('approved','Fully Approved'),('rejected','rejected')],string='State')

    def action_credit_report_button(self):
        data = {
            'subscription_id': self.subscription_id.ids,
            'state': self.state,
        }
        return self.env.ref('recurring_subscription.action_report_credit').report_action(None, data)

    def action_print_credit_xlsx(self):
        data = {

            'subscription_id': self.subscription_id.ids,
            'state': self.state,
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'credit.report.wizard',
                     'options': json.dumps(data, default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Credit Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report2(self, data, response):

        query = """ SELECT cr.id ,sub.name as SubscriptionName,res.name AS customer,cr.credit_amount, cr.state, bill.applied_credit as applied FROM recurring_subscription_credit AS cr  
        LEFT JOIN recurring_subscription AS sub ON cr.recurring_subscription_id = sub.id LEFT JOIN res_partner AS res ON sub.customer_id = res.id 
        LEFT JOIN billing_schedule AS bill ON bill.selected_credit_id = cr.id WHERE 1=1 """

        cr = data['subscription_id']
        if len(cr) == 1:
            credit_id = int(cr[0])
            query += " AND sub.id = %s" % credit_id
        elif cr:
            credits_id = str(tuple(cr))
            query += " AND sub.id IN %s" % credits_id
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
        query += " ORDER BY cr.id"
        self.env.cr.execute(query)
        docs = self.env.cr.dictfetchall()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('docs')
        sheet.set_column(1, 1, 15)
        sheet.set_column(2, 2, 15)
        sheet.set_column(3, 3, 15)
        sheet.set_column(4, 4, 15)
        sheet.set_column(5, 5, 15)
        sheet.set_column(6, 6, 15)
        sheet.set_column(7, 7, 15)
        border = workbook.add_format({'border': 1, 'align': 'left'})
        bold = workbook.add_format({'border': 1, 'align': 'left','bold': True})
        head = workbook.add_format({ 'bold': True, 'font_size': 24,
            'align': 'center','valign': 'vcenter','border': 1 })
        title = workbook.add_format({'bold': True, 'align': 'left',
            'valign': 'top','border': 1 })
        cell_format = workbook.add_format({'text_wrap': True, 'valign': 'top', 'font_size': 10,'border': 1 })
        company = self.env.company
        street = company.street
        street2 = company.street2
        city = company.city
        zip_code = company.zip
        country = company.country_id.name
        state = company.state_id.name

        full_address = f"{street} {street2}, {city}, {state} {zip_code}, {country}"
        sheet.merge_range('B2:G5', 'Credit Report', head)
        sheet.merge_range('B6:C7', company.name, title)
        sheet.merge_range('D6:E7', full_address, cell_format)
        if len(set(doc['state'] for doc in docs)) == 1:
            state =docs[0]['state']
            sheet.merge_range('B11:C11', 'state', bold)
            sheet.merge_range('D11:E11', state, border)
        if len(set(doc['customer'] for doc in docs)) == 1:
            customer=docs[0]['customer']
            sheet.merge_range('B12:C12', 'customer', bold)
            sheet.merge_range('D12:E12', customer, border)
        if len(set(doc['subscriptionname'] for doc in docs)) == 1:
            sub=docs[0]['subscriptionname']
            sheet.merge_range('B13:C13', 'subscriptionname', bold)
            sheet.merge_range('D13:E13', sub, border)
        unique_state = len(set(doc['state'] for doc in docs)) ==1
        unique_customer = len(set(doc['customer'] for doc in docs)) == 1
        unique_sub = len(set(doc['subscriptionname'] for doc in docs)) == 1

        if not unique_state and not unique_customer and not unique_sub:
            sheet.merge_range('B15:B16', 'Sl.No', bold)
            sheet.merge_range('C15:C16', 'Subscription', bold)
            sheet.merge_range('D15:D16', 'Customer', bold)
            sheet.merge_range('E15:E16', 'Credit Amount', bold)
            sheet.merge_range('F15:F16', 'Amount Applied', bold)
            sheet.merge_range('G15:G16', 'State', bold)

        elif not unique_state and not unique_customer and unique_sub:
            sheet.merge_range('B15:B16', 'Sl.No', bold)
            sheet.merge_range('C15:C16', 'Customer', bold)
            sheet.merge_range('D15:D16', 'Amount', bold)
            sheet.merge_range('E15:E16', 'Total Credit Applied', bold)
            sheet.merge_range('F15:F16', 'State', bold)

        elif not unique_state and unique_customer and not unique_sub:
            sheet.merge_range('B15:B16', 'Sl.No', bold)
            sheet.merge_range('C15:C16', 'Subscription', bold)
            sheet.merge_range('D15:D16', 'Amount', bold)
            sheet.merge_range('E15:E16', 'Total Credit Applied', bold)
            sheet.merge_range('F15:F16', 'State', bold)

        elif not unique_state and unique_customer and unique_sub:
            sheet.merge_range('B15:B16', 'Sl.No', bold)
            sheet.merge_range('C15:C16', 'Amount', bold)
            sheet.merge_range('D15:D16', 'Total Credit Applied', bold)
            sheet.merge_range('E15:E16', 'State', bold)

        elif unique_state and unique_customer and unique_sub:
            sheet.merge_range('B15:B16', 'Sl.No', bold)
            sheet.merge_range('C15:C16', 'Amount', bold)
            sheet.merge_range('D15:D16', 'Total Credit Applied', bold)

        elif unique_state and unique_customer and not unique_sub:
            sheet.merge_range('B15:B16', 'Sl.No', bold)
            sheet.merge_range('C15:C16', 'Subscription', bold)
            sheet.merge_range('D15:D16', 'Amount', bold)
            sheet.merge_range('E15:E16', 'Total Credit Applied', bold)

        elif unique_state and not unique_customer and unique_sub:
            sheet.merge_range('B15:B16', 'Sl.No', bold)
            sheet.merge_range('C15:C16', 'Customer', bold)
            sheet.merge_range('D15:D16', 'Amount', bold)
            sheet.merge_range('E15:E16', 'Total Credit Applied', bold)

        elif unique_state and not unique_customer and not unique_sub:
            sheet.merge_range('B15:B16', 'Sl.No', bold)
            sheet.merge_range('C15:C16', 'Subscription', bold)
            sheet.merge_range('D15:D16', 'Customer', bold)
            sheet.merge_range('E15:E16', 'Amount', bold)
            sheet.merge_range('F15:F16', 'Total Credit Applied', bold)

        row = 16
        col = 1
        for doc in docs:
            sheet.write(row, col, doc['id'], border)
            col += 1
            if len(set(doc['subscriptionname'] for doc in docs)) != 1:
                sheet.write(row, col, doc['subscriptionname'], border)
                col += 1
            if len(set(doc['customer'] for doc in docs)) != 1:
                sheet.write(row, col, doc['customer'], border)
                col += 1
            sheet.write(row, col, doc['credit_amount'], border)
            col += 1
            sheet.write(row, col, doc['applied'], border)
            col += 1
            if len(set(doc['state'] for doc in docs)) != 1:
                sheet.write(row, col, doc['state'], border)
            col = 1
            row += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()