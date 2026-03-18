# -*- coding: utf-8 -*-

from odoo import fields, models ,api



class ResPartner(models.Model):
    _inherit = "res.partner"

    last_reference_date = fields.Date(string="Last Reference Date", readonly=True)
    restricted = fields.Boolean("Restricted")
    restricted_count = fields.Integer(string="Restricted Count")