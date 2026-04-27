# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions

class ProjectTask(models.Model):
    _inherit = "project.task"
    _description = "Project Task"


    @api.model_create_multi
    def create(self, vals_list):
        for order in vals_list:
            print('create', order)
        return super().create(vals_list)

    @api.onchange('stage_id')
    def onchange_stage_id(self):
        print('onchange_stage_id')
        for order in self:
            if order.stage_id.name == 'In progress':
                print('onchange', order)
    # def write(self, vals):
    #     for order in vals:
    #         if self.stage_id.name=='In Progress':
    #             print('inprogress', self    )
    #     return super().write(vals)