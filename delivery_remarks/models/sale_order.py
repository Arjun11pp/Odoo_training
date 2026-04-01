# -*- coding: utf-8 -*-

from odoo import api, fields, models,_
from odoo.exceptions import UserError


class SalesOrder(models.Model):
    """ inherits from Sale Order """
    _inherit = "sale.order"

    delivery_remark=fields.Text('Delivery Remark')
    is_urgent_delivery=fields.Boolean('Urgent Delivery')
    preferred_delivery_time=fields.Selection([('morning','Morning'),('afternoon','Afternoon'),('evening','Evening')])

    discount_approved=fields.Boolean('Discount Approved',readonly=True,copy=False)
    discount_approved_by=fields.Many2one('res.users',readonly=True,copy=False)

    def action_sale_order_discount(self):
        """ Sale Order Approve Discount  button function """
        print(self)
        has_discount=False
        for order in self.order_line:
            if order.discount>0:
                has_discount=True

        if has_discount == False:
            raise UserError('No Discount Applied')
        else:
            self.write({'discount_approved':True})
            self.write({'discount_approved_by':self.env.user.id})
            self.message_post(  body=_(
                    " Discount approved by  %(username)s",
                     username=self.env.user.name
                ))