# -*- coding: utf-8 -*-

from odoo import fields, models,api,_
from odoo.exceptions import ValidationError


class FleetServiceOrder(models.Model):
    _name = 'fleet.service.order'

    name=fields.Char(string='Name', default=lambda self: _('New'),readonly=True)
    vehicle_id=fields.Many2one('fleet.vehicle')
    technician_id=fields.Many2one('hr.employee')
    service_date=fields.Date(string='Service Date')
    state=fields.Selection([('draft','Draft'),('confirmed','Confirmed'),('progress','In progress'),('done','Done'),('cancel','Cancelled')],default='draft')
    part_ids=fields.One2many('fleet.service.order.part','order_id',string='Part IDs')
    checklist_ids=fields.One2many('fleet.service.order.checklist','order_id',string='Checklist IDs')
    parts_total=fields.Float('Total Parts',compute='_compute_total')
    labour_cost=fields.Float('Labour Cost')
    grand_total=fields.Float('Grand Total',compute='_compute_grand_total')
    check_list_progress=fields.Float('Checklist Progress',compute='_compute_check_list_progress',default=0.0)
    type_ids=fields.Many2many('checklist.type',string='Type')

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            if val.get('name', _('New')) == _('New'):
                val['name'] = self.env['ir.sequence'].next_by_code('fleet.service.order')
        return super().create(vals)


    def _compute_total(self):
        total = 0
        for order in self.part_ids:

            total+=order.quantity*order.unit_price
        self.write({'parts_total':total})


    def _compute_grand_total(self):
        g_total=self.parts_total+self.labour_cost
        self.write({'grand_total':g_total})


    def _compute_check_list_progress(self):
        final=0
        for order in self:
            counts=len(order.checklist_ids.filtered(lambda l: l.is_done==True))
            total_checklist=len(order.checklist_ids.ids)
            if total_checklist>0:
                final=(counts/total_checklist)*100
        self.write({'check_list_progress':final})

    def action_fleet_service_confirm(self):
        for order in self:
            if order.part_ids:
                self.write({'state':'confirmed'})
            else:
                raise  ValidationError('No parts')

    def action_start_service(self):
        for order in self:
            if order.technician_id:
                self.write({'state':'progress'})
                if order.check_list_progress == 100 :
                    self.write({'state': 'done'})
            else:
                raise ValidationError(' technician is not selected')

    def action_fleet_cancel (self):
       self.write({'state':'cancel'})

    def action_fleet_service_generate(self):
        for order in self:
            if order.checklist_ids:
                return {
                    'warning': {
                        'title':'already checklist exists',
                        'message': 'already checklist exists'
                    }
                }
            else:
                for doc in order.type_ids:
                    self.env['fleet.service.order.checklist'].create({
                        'order_id': order.id,
                        'task_name': doc.name,

                    })
