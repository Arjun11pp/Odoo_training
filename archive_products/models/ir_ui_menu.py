# -*- coding: utf-8 -*-

from odoo import models,fields

class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    menu_id = fields.Many2many('res.users',string="Menu")