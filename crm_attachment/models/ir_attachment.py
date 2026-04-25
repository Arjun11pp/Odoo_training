# -*- coding: utf-8 -*-

from odoo import fields,models,api

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'
    _description = 'CRM Attachment'

    opportunity_id = fields.Many2one('crm.lead',string='Opportunity')

    @api.model_create_multi
    def create(self, vals_list):
        """ links opportunity to the attachment """
        for vals in vals_list:
            if vals.get('res_model') == 'crm.lead':
                vals['opportunity_id']=vals['res_id']
        return super().create(vals_list)

    def write(self, vals):
        """ links opportunity to the attachment """
        if vals.get('res_model') == 'crm.lead':
            vals['opportunity_id'] = vals['res_id']
        res = super().write(vals)
        return res

    def unlink(self):
        """ calls compute attachment method upon deletion """
        opp_id=self.opportunity_id
        res = super().unlink()
        if opp_id:
            opp_id._compute_attachment_count()
        return res