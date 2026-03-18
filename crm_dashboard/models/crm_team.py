# -*- coding: utf-8 -*-
from odoo import models, fields,api

class CrmTeam(models.Model):
    """Inherits crm.team and created a new many2one  field  related with crm.stage model"""
    _inherit = 'crm.team'

    lead_state_id = fields.Many2one('crm.stage', string='Lead State')