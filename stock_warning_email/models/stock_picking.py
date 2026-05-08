# -*- coding: utf-8 -*-

from odoo import  models

class StockPicking(models.Model):
    """ Inherits stock.picking model """
    _inherit = "stock.picking"
    _description = 'Inherits Stock Picking model'

    def button_validate(self):
        """ Override button validate function from stock.picking model to check the threshold limit of the product and sends warning email to warehouse manager """
        quant = 0
        for rec in self.product_id:
            product = self.env['inventory.warning'].search([('product_id', '=', rec.id)])
            if product:
                location = self.env['stock.quant'].search([('product_id', '=', rec.id)]).mapped('location_id')
                for loc in location:
                    warehouse_id = loc.warehouse_id
                    if warehouse_id:
                        locations = loc
                        manager_id = warehouse_id.manager_id
                        for locs in locations:
                            quant = sum(self.env['stock.quant'].search(
                            [('location_id', '=', locs.id), ('product_id', '=', rec.id)]).mapped('quantity'))
                if quant and quant <= product.quantity:
                    template = self.env.ref('stock_warning_email.inventory_alert_email_template')
                    email_values = {"subject": f"{rec.name} product stock alert .",
                                    'email_from': self.env.user.email, 'email_to': manager_id.email, }
                    template.send_mail(product.id, force_send=True, email_values=email_values)
        return super(StockPicking, self).button_validate()

