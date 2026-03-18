# -*- coding: utf-8 -*-

from odoo import fields, models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    purchase_order_id_mat= fields.Many2one(comodel_name='material.request',string="Purchase Order")
