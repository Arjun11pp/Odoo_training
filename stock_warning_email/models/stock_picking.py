# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions

class StockPicking(models.Model):
    _inherit = "stock.picking"
    _description = 'Inherits Stock Picking model'

    def button_validate(self):
        """ super button validate function """

        print('ids', self.product_id)
        warehouse_id = 0
        locations = []
        quant = 0
        for rec in self.product_id:
            print('rec', rec)
            product = self.env['inventory.warning'].search([('product_id', '=', rec.id)])
            if product:
                # stock_location = self.env['stock.quant'].search([('product_id', '=', rec.id)])
                location = self.env['stock.quant'].search([('product_id', '=', rec.id)]).mapped('location_id')
                for loc in location:
                    # print('loc',loc)
                    warehouse_id = loc.warehouse_id
                    print('warehouse_id', warehouse_id)
                    if warehouse_id:
                        locations = loc
                        manager_id = warehouse_id.manager_id
                        for locs in locations:
                            quant = sum(self.env['stock.quant'].search(
                            [('location_id', '=', locs.id), ('product_id', '=', rec.id)]).mapped('quantity'))
                if quant and quant <= product.quantity:
                    print('123')
                    template = self.env.ref('stock_warning_email.inventory_alert_email_template')
                    email_values = {"subject": f"{rec.name}  stock alert .",
                                    'email_from': self.env.user.email, 'email_to': manager_id.email, }
                    template.send_mail(rec.id, force_send=True, email_values=email_values)
                print('warehouse_id', warehouse_id, manager_id.name, quant)
        print('res', self.abc)
        res = super(StockPicking, self).button_validate()

        return res
