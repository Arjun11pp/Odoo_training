# -*- coding: utf-8 -*-

from odoo import fields, models,api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = "Inherits res config Settings"

    product_location_toggle = fields.Boolean(string='Choose location ',config_parameter='pos_product_quantity.product_location_toggle')
    product_location_id = fields.Many2one('stock.location',string='Choose Location',readonly=False,config_parameter='pos_product_quantity.product_location_id')

    @api.onchange('product_location_id')
    def _onchange_product_location_id(self):
        """ passing selected location from configuration settings"""
        for order in self:
            products = self.env['product.product'].search([])
            product_tmpl = self.env['product.template'].search([])
            products.write({'selected_stock_location_id': order.product_location_id.id})
            product_tmpl.write({'selected_stock_location_id': order.product_location_id.id})

