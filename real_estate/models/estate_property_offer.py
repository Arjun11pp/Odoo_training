from email.policy import default

from datetime import timedelta

from odoo.exceptions import UserError
from odoo.tools import date_utils
from datetime import date

from odoo import fields, models,api


class real_estate_offer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Offer'
    _order = 'price desc'

    price=fields.Float(string='Price')
    status=fields.Selection([('accepted','Accepted'),('refused','Refused')],copy=False)
    partner_id=fields.Many2one('res.partner',string='Partner' ,required=True)
    property_id=fields.Many2one('estate.property',string='Property' ,required=True, ondelete='cascade')
    validity=fields.Integer(default=7)
    create_date=fields.Date(string='Created Date',default=fields.Date.today())
    date_deadline=fields.Date(string='Date of Deadline',compute="_compute_date", inverse="_inverse_date")
    property_type_id=fields.Many2one(related='property_id.property_type_id', store=True )


    _check_ofr_price = models.Constraint(
        'CHECK(price >= 0 )',
        'The Offer price should be positive.')

    @api.depends('validity','create_date','date_deadline')
    def _compute_date(self):
        for res in self:
            if res.create_date:
                res.date_deadline=date_utils.add(value=res.create_date,days=res.validity)
            else:
                res.date_deadline=0
    def _inverse_date(self):
        for res in self:
            if res.date_deadline:
                res.validity=str((res.date_deadline-res.create_date).days)

    def action_confirm(self):
        for res in self:
            if res.property_id.selling_price==0:
                res.status = 'accepted'
                res.property_id.selling_price=res.price
                res.property_id.property_buyer_id=res.partner_id
            elif res.status=='refused' and res.property_id.selling_price==0:
                res.status = 'accepted'
                res.property_id.selling_price = res.price
                res.property_id.property_buyer_id = res.partner_id
            else:
                raise UserError('An Offer has been already accepted')


    def action_cancel(self):
        for res in self:
            if res.status=='accepted':
                raise UserError('An Offer has been already accepted')
            else:
                res.status = 'refused'

    @api.model_create_multi
    def create(self, vals):
        print(123123, vals)

        for val in vals:
            # print("hello", val)
            record=self.env['estate.property'].browse(val['property_id'])
            # max_value=max(record.mapped('offer_ids.price'))

            # print("hello", max_value)
            # print("record", record.offer_ids)
            # if record.price < max_value:
            #     raise UserError('An Offer has been already accepted')

            record.state='offer'

        return super().create(vals)




