# -*- coding: utf-8 -*-

from odoo import fields, models

class ResUser(models.Model):
    _inherit = 'res.users'
    _description = 'Project Task'

    task_tags_ids = fields.Many2many(comodel_name='project.tags', string='Tags')