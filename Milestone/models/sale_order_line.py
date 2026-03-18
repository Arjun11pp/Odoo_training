# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.fields import Command


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    milestone=fields.Integer(string="Milestone")


