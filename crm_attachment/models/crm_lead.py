# -*- coding: utf-8 -*-

from odoo import fields,models,api

class CRMLead(models.Model):
    _inherit = 'crm.lead'
    _description = 'Inherits CRM Lead model'

    attachment_count = fields.Integer(string='Attachment Count', compute='_compute_attachment_count',store=False)

    @api.depends('message_ids','message_attachment_count')
    def _compute_attachment_count(self):
        print('111111111111111111111111')
        """ Compute function to find attachment count """
        count = len(self.env['ir.attachment'].search([('opportunity_id', '=', self.id)]).ids)
        print('count111', count)
        self.write({'attachment_count': count})

    def action_get_crm_attachments(self):
        """ Get CRM attachments """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'CRM Lead Attachments',
            'view_mode': 'list,form',
            'res_model': 'ir.attachment',
            'domain': [('opportunity_id', '=', self.id)],
        }
