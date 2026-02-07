


from odoo import models, fields, api


class SaleDate(models.Model):
    _inherit = 'sale.order'

    new_date = fields.Integer(string="New Date", compute="_compute_new_date",store=True)
    today_date=fields.Datetime.now()
    @api.depends('date_order')
    def _compute_new_date(self):
        for order in self:
            order.new_date = str((order.date_order - order.today_date).days)