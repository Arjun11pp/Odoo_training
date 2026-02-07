# -*- coding: utf-8 -*-
import random
from odoo import models,fields,_
from odoo import Command
from odoo.exceptions import UserError


class MaterialRequest(models.Model):
    _name = "material.request"
    _rec_name = 'req_name'

    _inherit = ['mail.thread', 'mail.activity.mixin']

    req_name =fields.Char(string="Name")
    employee_id= fields.Many2one(comodel_name='res.partner', string="Employee",default=lambda self: self.env.user.partner_id,readonly=True)
    request_line_ids=fields.One2many(comodel_name='material.products',inverse_name="request_id")
    date=fields.Date(string="Request Date",default=fields.Date.today())
    state=fields.Selection([("draft","Draft"),('submitted','Submitted'),('approved','Manager Approved'),('head','Head Approved'),('reject','Rejected')],string="State" ,default="draft")

    def action_get_purchase_orders(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'purchase orders',
            'view_mode': 'list,form',
            'res_model': 'purchase.order',
            'domain': [('purchase_order_id', '=', self.ids)],
            'context': "{'create': False}"
        }

    def action_get_internal_transfer(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Internal transfer',
            'view_mode': 'list,form',
            'res_model': 'stock.picking',
            'domain': [('transfer_id', '=', self.ids)],
            'context': "{'create': False}"
        }

    def action_send(self):
        self.write({'state':'submitted'})

    def action_confirm(self):
        self.write({'state':'approved'})

    def action_reject(self):
        self.write({'state':'reject'})

    def action_head_approval(self):
        for order in self.request_line_ids:
            if order.request_type == 'po':
                vendors = self.env['product.supplierinfo'].search([('product_id', '=', order.product_id)])
                if vendors:
                    for vendor in vendors:
                        self.env['purchase.order'].create({
                            "partner_id": vendor.partner_id.id,
                            'purchase_order_id': self.id,
                            "order_line": [
                                Command.create({
                                    'product_id': order.product_id.id,
                                    'name': order.product_id.name,
                                    'price_unit': vendor.price,
                                    'product_qty': order.quantity,
                                }),
                            ]})
                else :
                    random_vendor=random.choice(self.env['res.partner'].search([]).ids)
                    self.env['purchase.order'].create({
                            "partner_id": random_vendor,
                        'purchase_order_id': self.id,
                            "order_line": [
                                Command.create({
                                    'product_id': order.product_id.id,
                                    'price_unit': order.product_id.lst_price,
                                    'product_qty': order.quantity,
                                }),
                            ]})
            else:
                picking=self.env.ref('stock.picking_type_internal').id
                self.env['stock.picking'].create({
                    'picking_type_id': picking ,
                    'transfer_id': self.id,
                    'partner_id': self.employee_id.id,
                    'location_id': order.source_location_id.id,
                    'location_dest_id': order.destination_location_id.id ,
                    'move_ids': [Command.create({
                        'product_id': order.product_id.id,
                        'product_uom_qty': order.quantity,

                    })],
                })
        self.message_post(
                    body=_("Requisition Head has been Approved"),)
        self.write({'state':'head'})


