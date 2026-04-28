# -*- coding: utf-8 -*-

from odoo import api, models
from odoo import fields
from odoo.exceptions import ValidationError

class ProjectTask(models.Model):
    _inherit = "project.task"
    _description = "Project Task"

    task_state_id= fields.Many2one('project.task.type',string="Task State")

    @api.onchange('stage_id')
    def onchange_new_task_state(self):
        current_user=self.env.user.id
        emp_id = self.env['hr.employee'].search([('user_id', '=', current_user)])
        for order in self:
            if order.task_state_id == self.stage_id:
                order.write({'timesheet_ids':[
                                fields.Command.create( {
                                    'date': fields.Date.today(),
                                    'employee_id': emp_id,})
                                ] })

    @api.onchange('tag_ids')
    def tag_onchange(self):
        for order in self:
            if order.tag_ids:
                user_id=self.env['res.users'].search([('task_tags_ids','in',order.tag_ids.ids)],limit=1)
                order.user_ids=user_id

    @api.onchange('state')
    def onchange_task_state(self):
        for order in self:
            if order.task_state == 'done':
                if order.timesheet_ids:
                    for timesheets in order.timesheet_ids:
                        if timesheets.unit_amount == 0:
                            raise ValidationError('Times sheet hour is zero')
