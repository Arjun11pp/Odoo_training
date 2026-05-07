# -*- coding: utf-8 -*-

from odoo import fields, models, api

class ProductProduct(models.Model):
    _inherit = 'product.product'
    _description = 'Product Template'

    # @api.depends('qty_available')
    # def on_quantity_change(self):
    #     print('_compute_quantities')
    #     result = super(ProductProduct,self)._compute_quantities()
    #     warehouse_id=0
    #     locations=[]
    #     quant=0
    #     for rec in self:
    #         product=self.env['inventory.warning'].search([('product_id','=',rec.id)])
    #         if product:
    #             stock_location=self.env['stock.quant'].search([('product_id','=',rec.id)])
    #             location=self.env['stock.quant'].search([('product_id','=',rec.id)]).mapped('location_id')
    #             for loc in location:
    #                 # print('loc',loc)
    #                 warehouse_id=loc.warehouse_id
    #                 print('warehouse_id',warehouse_id)
    #                 if warehouse_id:
    #                     locations=loc
    #                     manager_id=warehouse_id.manager_id
    #                 for locs in locations:
    #                     quant=sum(self.env['stock.quant'].search([('location_id','=',locs.id),('product_id','=',rec.id)]).mapped('quantity'))
    #             if quant and quant <= product.quantity:
    #                 print('123')
    #                 template = self.env.ref('stock_warning_email.inventory_alert_email_template')
    #                 email_values = {'email_from': self.env.user.email, 'email_to': manager_id.email ,}
    #                 template.send_mail(rec.id, force_send=True, email_values=email_values)
    #                 # self.message_post_with_source(template, subtype_xmlid='stock_warning_email.inventory_alert_email_template', )
    #             print('warehouse_id',warehouse_id,manager_id.name,quant)
    #
    #
    #     return result