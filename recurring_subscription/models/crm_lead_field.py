# -*- coding: utf-8 -*-
from odoo import fields,models

class CrmLeadField(models.Model):
    _inherit = 'crm.lead'

    order_id = fields.Char(string="Order ID",required=True)

    _order_id_unique = models.Constraint(
        'Unique(order_id)','Order Id should be unique'
    )