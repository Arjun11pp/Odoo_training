# -*- coding: utf-8 -*-
from odoo import models,fields

class Sale_Order(models.Model):
    _inherit = 'sale.order'

    state=fields.Selection(selection_add=[
        ('done',"Done"),
        ('sale', )
    ])