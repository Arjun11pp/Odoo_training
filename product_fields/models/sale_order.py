# -*- coding: utf-8 -*-
from dateutil.utils import today

from odoo import models,fields,api
from odoo.tools import date_utils


class SaleOrder(models.Model):
    _inherit = "sale.order"

    prime_customer_id = fields.Boolean(related='partner_id.prime_customer',string="Is Prime Customer")

    def action_customer_button(self):
        p_list={}
        print(self.partner_id.name)
        sale_orders=len(self.search([('partner_id','=',self.partner_id.id)]))
        sale_order_amount=sum(self.search([('partner_id','=',self.partner_id.id)]).mapped('amount_total'))
        print("sale order count",sale_orders)
        print("sale order total",sale_order_amount)
        sale_orders_product=self.search([('partner_id','=',self.partner_id.id)])

        for record in sale_orders_product:
            for rec in record.order_line:
                if rec.product_template_id.name not in p_list:
                    p_list[rec.product_template_id.name] = rec.product_uom_qty
                else :
                    quantity =int(p_list[rec.product_template_id.name])+rec.product_uom_qty
                    p_list[rec.product_template_id.name]=quantity
        for key, value in p_list.items():
            print(f"Product : {key}, Quantity: {value}")
        lar=max(p_list.values())
        small=min(p_list.values())
        # print('max', lar)
        for key, value in p_list.items():
            if value==lar:
                print(f"Top selling Product : {key}, Quantity: {value}")
        for key, value in p_list.items():
            if value==small:
                print(f"least  selling Product : {key}, Quantity: {value}")

        sale_orders_no=self.search([('partner_id','=',self.partner_id.id)]).filtered(lambda l:l.date_order.month==2)
        print("sale orders in current month",len(sale_orders_no))

