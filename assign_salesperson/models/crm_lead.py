# -*- coding: utf-8 -*-

from odoo import fields, models,api
from odoo.exceptions import ValidationError

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    _description = 'CRM Lead'

    @api.model_create_multi
    def create(self, vals):
        res=super().create(vals)
        partner_country_id=res.partner_id.country_id
        user_id=self.env['res.users'].search([('country_id','=',partner_country_id)],limit=1)
        if user_id:
            res.write({'user_id':user_id.id})
        self.env['mail.activity'].create({
            'res_model_id': self.env['ir.model']._get('crm.lead').id,
            'res_id': res.id,
            'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
            'summary': 'Follow up with customer',
            'note': 'Please call the customer to discuss the quote details.',
            'user_id': self.user_id.id or self.env.user.id,
            'date_deadline': fields.Date.today(),
        })
        self.env['mail.activity'].create({
            'res_model_id': self.env['ir.model']._get('crm.lead').id,
            'res_id': res.id,
            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
            'summary': 'Follow up with customer',
            'note': 'Follow-up on activity.',
            'user_id': self.user_id.id or self.env.user.id,
            'date_deadline': fields.Date.today(),
        })
        return res

    def write(self, vals):
        stage_id=self.env.ref('crm.stage_lead4').id
        activity_id=self.env['mail.activity'].search([('active','=',False),('res_model','=','crm.lead'),('res_id','=',self.id)])
        if not activity_id and self.stage_id.id == stage_id:
            raise ValidationError('At least one activity must be completed')
        else:
            return super(CrmLead, self).write(vals)

