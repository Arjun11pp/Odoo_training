# -*- coding: utf-8 -*-

from  odoo import api, fields, models
from odoo.exceptions import ValidationError

class AccountMove(models.Model):
    """ Invoice account moves """
    _inherit = "account.move"

    shipment_count = fields.Integer(string="Shipment Count",default=0,compute="_compute_shipment_count")
    shipment_status=fields.Selection([('draft','Draft'),('waiting','Waiting Another Operation'),('confirmed','Waiting') ,('assigned','Ready'),('done','Done')
                                      ,('cancel','Cancelled')],string="Delivery Status", default="draft", readonly=True, compute="_compute_shipment_status")

    def action_post(self):
        """ overriding invoice confirm button """
        if self.shipment_status == 'cancel' :
            raise ValidationError('Invoice cannot be confirmed because the delivery order is cancelled')
        res = super().action_post()
        return res

    def _compute_shipment_status(self):
        """ Compute shipment status """
        delivery_orders = self.line_ids.sale_line_ids.order_id.picking_ids
        if delivery_orders:
            latest=delivery_orders[-1]
            print('latest',latest)
            self.write({'shipment_status': latest.state})
        else:
            self.write({'shipment_status': 'draft'})

    def _compute_shipment_count(self):
        """ Compute shipment count """
        delivery_orders = self.line_ids.sale_line_ids.order_id.picking_ids
        count_no = len(delivery_orders)
        self.write({'shipment_count': count_no})

    def action_get_delivery_details(self):
        """ Returns the details of the delivery """
        delivery_orders = self.line_ids.sale_line_ids.order_id.picking_ids
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'delivery_details',
            'view_mode': 'list,form',
            'res_model': 'stock.picking',
            'domain': [('id', 'in', delivery_orders.ids)],
            'context': "{'create': False}"
        }