# -*- coding: utf-8 -*-

from odoo import fields,models,api

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'
    _description = 'CRM Attachment'

    opportunity_id = fields.Many2one('crm.lead',string='Opportunity')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('res_model') == 'crm.lead':
                vals['opportunity_id']=vals['res_id']
        return super().create(vals_list)

    def write(self, vals):
        if vals.get('res_model') == 'crm.lead':
            vals['opportunity_id'] = vals['res_id']
        res = super().write(vals)
        return res