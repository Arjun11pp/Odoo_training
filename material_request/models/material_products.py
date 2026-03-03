# -*- coding: utf-8 -*-

from odoo import models,fields,api

class MaterialProducts(models.Model):
    _name = "material.products"

    request_id = fields.Many2one(string="Request",comodel_name='material.request')
    product_id = fields.Many2one(string="Product",comodel_name='product.product')
    quantity = fields.Float(string="Quantity",default=1)
    request_type = fields.Selection([('po', 'Purchase Order'), ('internal', 'Internal transfer')], required=True, string="Request Type")
    source_location_id = fields.Many2one(comodel_name='stock.location',string="Source Location")
    destination_location_id=fields.Many2one(comodel_name='stock.location',string="Destination Location")

    @api.onchange('request_type')
    def onchange_request_type(self):
        print("123")
        for rec in self:
            if rec.request_type == 'po':
                # rec.write({'source_location_id':False})
                rec.source_location_id = False

