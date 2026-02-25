# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import UserError

class ProjectTask(models.Model):
    _inherit = "project.task"

    hours_per_day = fields.Float("Hours per Day")

    @api.onchange('timesheet_ids')
    def onchange_timesheet_ids(self):
        unique_dates = set()
        for rec in self.timesheet_ids:
            if rec.date:
                unique_dates.add(rec.date)
        for dates in unique_dates:
            t_ids = self.timesheet_ids.filtered(lambda t: t.date == dates )
            for emp_id in t_ids.employee_id:
                emp1=t_ids.filtered(lambda e: e.employee_id == emp_id)
                total=sum(i.unit_amount for i in emp1)
                if total > self.hours_per_day:
                    raise UserError("Time spend is greater than the hour per day")