# -*- coding: utf-8 -*-

from odoo import fields, models,api

class ChecklistType(models.Model):
    _name = 'checklist.type'

    name = fields.Char('Name')