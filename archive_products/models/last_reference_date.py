# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields,api
from odoo.exceptions import ValidationError, UserError


class LastReferenceDate(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        partner=self.partner_id
        last_date=partner.last_reference_date
        date_90_days_ago = (fields.Datetime.today() - timedelta(days=90)).date()
        if last_date and last_date < date_90_days_ago:
                raise ValidationError('vendor hasn’t supplied anything for more than 90 days,')
        result=super(LastReferenceDate,self).button_confirm()
        date2=self.date_approve.date()
        # date2=(fields.Datetime.today() - timedelta(days=91)).date()
        partner.write({'last_reference_date': date2})
        return result


    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        partner = self.partner_id
        last_date = partner.last_reference_date
        date_90_days_ago = (fields.Datetime.today() - timedelta(days=90)).date()
        if last_date and last_date < date_90_days_ago:
            return {
                'warning': {
                    'title': "Last Reference Date is more than 90 days ago",
                    'message': "vendor hasn’t supplied anything for more than 90 days."
                }
            }