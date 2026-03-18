# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import Command
from odoo import fields, models, api

class ArchiveProducts(models.Model):
    _inherit = "product.product"

    min_threshold=fields.Integer("Min Threshold" )


    def _compute_archived_products(self):
        r = {}
        self.sales_count = 0
        if not self.env.user.has_group('sales_team.group_sale_salesman'):
            return r
        date_from = fields.Date.today() - timedelta(days=90)
        done_states = self.env['sale.report']._get_done_states()
        domain = [('state', 'in', done_states),
            ('product_id', 'in', self.ids),
            ('date', '>=', date_from),]
        for product, product_uom_qty in self.env['sale.report']._read_group(domain, ['product_id'],['product_uom_qty:sum']):
            r[product.id] = product_uom_qty
        for product in self:
            if not product.id:
                product.sales_count = 0.0
                continue
            product.sales_count = product.uom_id.round(r.get(product.id, 0))
        return r

    # def action_archive_products(self):
    #     for rec in (self.search([('active', '=', True)])):
    #         products=rec.filtered(lambda p:p.sales_count == 0)
    #         for record in products:
    #             print(record)
    #             record.write({'active': False } )

    def _compute_quantities(self):
        result=super(ArchiveProducts,self)._compute_quantities()
        for rec in self:
            if rec.qty_available < rec.min_threshold:
                vendors = self.env['product.supplierinfo'].search([('product_id', '=', rec.id)])
                if vendors:
                    vendor=vendors[0]
                    po=self.env['purchase.order'].create({
                        "partner_id": vendor.partner_id.id,
                        "order_line": [
                            Command.create({
                                'product_id': rec.id,
                                'name': rec.name,
                                'price_unit': vendor.price,
                                'product_qty': vendor.min_qty,
                            }),]})
                    po.button_confirm()
                    picking = po.picking_ids
                    picking.button_validate()
        return result