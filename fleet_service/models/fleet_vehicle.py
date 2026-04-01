# -*- coding: utf-8 -*-

from odoo import fields, models,api

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    service_blocked=fields.Boolean(string="Service Blocked")