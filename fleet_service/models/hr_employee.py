# -*- coding: utf-8 -*-

from odoo import fields, models,api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_available_technician = fields.Boolean(string="Is Available Technician")
    vehicle_ids = fields.Many2many(string="Vehicle IDs",comodel_name='fleet.vehicle')