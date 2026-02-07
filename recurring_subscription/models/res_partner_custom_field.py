# -*- coding: utf-8 -*-
import re
import random
import string
from odoo import fields, models, api
from odoo.exceptions import ValidationError

class ResPartnerCustomField(models.Model):
    _inherit = "res.partner"

    establishment_id = fields.Char(string="Establishment ID",required=True,)
    account_id = fields.Many2one(comodel_name='partner.account.id', string="Account ID" ,ondelete='cascade',readonly=True)

    _name_uniques = models.Constraint(
        'UNIQUE(establishment_id)',
        'Establishment ID should be unique',)

    @api.constrains('establishment_id')
    def _compute_establishment_id(self):
        for record in self:
            alphabets = re.findall(r'[a-zA-Z]', record.establishment_id)
            numbers = re.findall(r'[0-9]', record.establishment_id)
            special_chars = re.findall(r'[!@#$%^&*()_+={}\[\]:;"\'<,>./?`~\\-]', record.establishment_id)
            if len(alphabets) < 3 or len(numbers) < 3 or len(special_chars) < 2:
                raise ValidationError("There must be at least 3 alphabets, numbers and 2 special characters!")

    @api.model_create_multi
    def create(self, vals):
        partner=super().create(vals)
        letters = ''.join((random.choice(string.ascii_letters) for i in range(3)))
        digits = ''.join((random.choice(string.digits) for i in range(3)))
        special_chars = ''.join((random.choice(string.punctuation) for i in range(2)))
        sample_list = list(letters + digits + special_chars)
        random.shuffle(sample_list)
        final_string = ''.join(sample_list)
        abs=self.env['partner.account.id'].create({'account_id': final_string , 'partner_id': partner.id})
        partner.account_id = abs.id
        return partner