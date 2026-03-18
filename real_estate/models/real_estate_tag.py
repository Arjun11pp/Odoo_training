from odoo import fields, models


class real_estate_tag(models.Model):
    _name = 'real.estate.tag'
    _description = 'Property Tag'
    _order = 'name'

    name = fields.Char(string='Property Tag', required=True)
    color = fields.Integer()
    _name_uniques = models.Constraint(
        'UNIQUE(name)',
        'Property Tag should be unique',
    )
