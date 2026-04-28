# -*- coding: utf-8 -*-

from odoo import fields, models,api

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    _description = 'CRM Lead'

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            print('vals', val,self)

        res=super().create(vals)
        print(res)
        self.env['mail.activity.schedule'].create({

        })

        return res
