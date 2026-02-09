# -*- coding: utf-8 -*-
from odoo import models, fields

class PartnerAccountId(models.Model):
    _name = 'partner.account.id'
    _description = 'Partner Account'
    _rec_name = 'account_id'

    account_id = fields.Char(string="Account ID" ,readonly=True,ondelete='cascade')
    partner_id = fields.Many2one(comodel_name='res.partner', string="Partner Account",readonly=True)
    _name_uniques = models.Constraint(
        'UNIQUE(account_id)',
        'Account ID should be unique',
    )