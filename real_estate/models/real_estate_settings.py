from itertools import count

from odoo import fields, models, api


class real_estate_settings(models.Model):
    _name='real.estate.type'
    _description = 'Property types'
    _order = 'name'
    

    name=fields.Char(string='Property Type',required=True)

    model_id = fields.One2many('estate.property' ,inverse_name='property_type_id')
    sequence=fields.Integer()
    button=fields.Char(compute='_compute_button')
    offer_ids=fields.One2many('estate.property.offer' ,inverse_name='property_type_id')
    offer_count=fields.Integer(compute='_compute_offer_count')

    @api.depends('offer_count')
    def _compute_offer_count(self):
        for rec in self:

            rec.offer_count = len(rec.offer_ids)

    def _compute_button(self):
        for prop in self:
            prop.button=prop.name


    _type_uniques = models.Constraint(
        'UNIQUE(name)',
        'Property Type should be unique',
    )