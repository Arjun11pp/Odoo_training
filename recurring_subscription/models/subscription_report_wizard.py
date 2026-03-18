# -*- coding: utf-8 -*-

import io
import json
from odoo import fields, models
from odoo.tools import date_utils, json_default
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter
class SubscriptionReportWizard(models.TransientModel):
    _name = "subscription.report.wizard"

    subscription_id = fields.Many2many('recurring.subscription',string="Subscription")
    duration=fields.Selection([('daily',"daily"),('weekly','Weekly'),('monthly','Monthly'),('yearly','Yearly'),('custom','Custom')],string="Duration")
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    company_id = fields.Many2one('res.company',string="Company", default=lambda self: self.env.company)

    def action_subscription_report_button(self):
        data={
            'subscription_id':self.subscription_id.ids,
            'duration':self.duration,
            'from_date':self.from_date,
            'to_date':self.to_date,
        }
        return self.env.ref('recurring_subscription.action_report_subscription').report_action(None,data)

    def action_print_xlsx(self):
        data = {
            'from_date': self.from_date,
            'to_date': self.to_date,
            'subscription_id': self.subscription_id.ids,
            'duration': self.duration,
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'subscription.report.wizard',
                     'options': json.dumps(data, default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Subscription Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        query = """ SELECT rs.sequence_number , rs.name  ,res.name AS customer,temp.name AS product,rs.recurring_amount,rs.total_credit,rs.state ,rs.terms_and_conditions ,bill.applied_credit as appliedcredit
                            FROM recurring_subscription AS rs LEFT JOIN res_partner res ON rs.customer_id = res.id LEFT JOIN product_product p ON rs.product_id = p.id
                            LEFT JOIN product_template temp ON p.product_tmpl_id = temp.id LEFT JOIN billing_schedule_recurring_subscription_rel as bs ON bs.recurring_subscription_id = rs.id 
                            LEFT JOIN billing_schedule as bill ON bill.id = bs.billing_schedule_id WHERE 1=1 """

        subscription = data['subscription_id']
        if len(subscription) == 1:
            sub = int(subscription[0])
            query += " AND rs.id = %s" % sub
        elif subscription:
            sub = str(tuple(subscription))
            query += " AND rs.id IN %s" % sub
        if data['duration'] == 'daily':
            query += " AND rs.date = '%s' " % (fields.Date.today())
        elif data['duration'] == 'weekly':
            start_date = date_utils.start_of(fields.Date.today(), "week")
            end_date = date_utils.end_of(fields.Date.today(), "week")
            query += " AND rs.date >= '%s' AND rs.date <= '%s' " % (start_date, end_date)
        elif data['duration'] == 'monthly':
            start_date = date_utils.start_of(fields.Date.today(), "month")
            end_date = date_utils.end_of(fields.Date.today(), "month")
            query += "  AND  rs.date >= '%s' AND rs.date <= '%s' " % (start_date, end_date)
        elif data['duration'] == 'yearly':
            start_date = date_utils.start_of(fields.Date.today(), "year")
            end_date = date_utils.end_of(fields.Date.today(), "year")
            query += " AND  rs.date >= '%s' AND rs.date <= '%s' " % (start_date, end_date)
        elif data['duration'] == 'custom':
            start_date = data['from_date']
            end_date = data['to_date']
            query += " AND  rs.date >= '%s' AND rs.date <= '%s' " % (start_date, end_date)
        query += " ORDER BY rs.sequence_number"
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
        border = workbook.add_format({'border': 1,'align': 'left'})
        title = workbook.add_format({'align': 'left','bold': True,'valign': 'top' })

        head = workbook.add_format(
            {'bold': True, 'font_size': 30, 'align': 'center', 'valign': 'vcenter'})
        company=self.env.company
        street = company.street
        street2 = company.street2
        city = company.city
        zip_code = company.zip
        country = company.country_id.name
        state = company.state_id.name

        full_address = f"{street} {street2}, {city}, {state} {zip_code}, {country}"
        cell_format = workbook.add_format({ 'text_wrap': True,  'valign': 'top' })
        sheet.merge_range('C2:H5', 'Subscription Report', head)
        sheet.merge_range('C6:D8', company.name, title)
        sheet.merge_range('E6:F8', full_address, cell_format)
        if len(set(doc['customer'] for doc in docs)) == 1:
            customer = docs[0]['customer']
            sheet.merge_range('B10:C10', 'customer', title)
            sheet.merge_range('D10:E10', customer, border)

        sheet.merge_range('B12:B13', 'Sl.No', title)
        sheet.merge_range('C12:C13', 'Subscription', title)
        if len(set(doc['customer'] for doc in docs)) != 1:
            sheet.merge_range('D12:D13', 'Customer', title)
            sheet.merge_range('E12:E13', 'Product', title)
            sheet.merge_range('F12:F13', 'Amount', title)
            sheet.merge_range('G12:G13', 'Total Credit Applied', title)
            sheet.merge_range('H12:H13', 'State', title)
        else:
            sheet.merge_range('D12:D13', 'Product', title)
            sheet.merge_range('E12:E13', 'Amount', title)
            sheet.merge_range('F12:F13', 'Total Credit Applied', title)
            sheet.merge_range('G12:G13', 'State', title)

        row = 13
        col = 1
        for doc in docs:
            sheet.write(row, col, doc['sequence_number'], border)
            col += 1
            sheet.write(row, col, doc['name'], border)
            col += 1
            if len(set(doc['customer'] for doc in docs)) != 1:
                sheet.write(row, col, doc['customer'], border)
                col += 1
            sheet.write(row, col, doc['product'].get('en_US'), border)
            col += 1
            sheet.write(row, col, doc['recurring_amount'], border)
            col += 1
            sheet.write(row, col, doc['total_credit'], border)
            col += 1
            sheet.write(row, col, doc['state'], border)
            col = 1
            row += 1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()