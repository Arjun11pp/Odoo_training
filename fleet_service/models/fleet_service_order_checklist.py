# -*- coding: utf-8 -*-

from odoo import fields, models, api
class FleetServiceOrderChecklist(models.Model):
    _name = 'fleet.service.order.checklist'
    _rec_name = 'task_name'

    order_id = fields.Many2one('fleet.service.order')
    task_name=fields.Char('Task Name')
    is_done = fields.Boolean('Is Done')
    note =fields.Text('Note')
