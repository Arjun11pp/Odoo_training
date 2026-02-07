# -*- coding: utf-8 -*-

from odoo import  models
from odoo.exceptions import UserError
from odoo.fields import Command


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_create_projects(self):
        orders=self.order_line
        if orders:
            milestones=set(self.order_line.mapped('milestone'))
            project = self.env['project.project'].create({
                'name': self.name,
            })
            for mile in milestones:
                task=self.order_line.filtered(lambda l: l.milestone == mile)
                self.env['project.task'].create([{
                    'name': "milestone " + str(mile),
                    'project_id': project.id,

                    'child_ids': [
                        Command.create({'name': "milestone  " + str(mile) +" " + i.name})
                        for i in task
                    ],
                }])
        else:
            raise UserError(' no products in order line')