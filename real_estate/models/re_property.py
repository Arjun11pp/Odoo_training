from email.policy import default

from magic.compat import CHECK

from odoo import models,fields,api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import date_utils, float_compare
from datetime import date
class Real_estate(models.Model):
    _name = "estate.property"
    _description = "Real estate"
    _order = "id desc"

    name=fields.Char(required=True)
    description=fields.Text()
    postcode=fields.Char()
    date_availability=fields.Date(
        string='Availability Date',
        copy=False,
        default=date_utils.add(date.today(),months=3)
    )
    expected_price=fields.Float(required=True)
    selling_price=fields.Float(readonly=True,copy=False,)
    bedrooms=fields.Integer(default=2)
    living_area=fields.Integer()
    facades=fields.Integer()
    garage=fields.Boolean()
    garden=fields.Boolean()
    garden_area=fields.Integer()
    garden_orientation=fields.Selection([('north','North'),('south','South'),('east','East'),('west','West')])
    active=fields.Boolean(default=False)
    state=fields.Selection([('new','New'), ('offer','Offer Received'),('accepted','Offer Accepted'),('sold','Sold'),('cancelled','Cancelled')],default='new',required=True,copy=False)
    property_type_id=fields.Many2one('real.estate.type',string='Property Type',required=True)
    property_salesman_id=fields.Many2one('res.users',string='Salesman',required=True,default=lambda self: self.env.user)
    property_buyer_id=fields.Many2one('res.partner',string='Buyer' )
    property_tag_id=fields.Many2many('real.estate.tag',string='Property Tag',required=True)
    offer_ids=fields.One2many('estate.property.offer','property_id',string='Offers')
    total = fields.Integer(string='Total Area',compute='_compute_balance')
    best_price=fields.Float(compute='_compute_best_price')
    line_ids = fields.One2many("real.estate.type", "model_id")

    _check_ex_price = models.Constraint(
        'CHECK(expected_price >= 0 )',
        'The Expected price should be positive.')

    _check_sel_price = models.Constraint(
        'CHECK(selling_price >= 0 )',
        'The Selling price should be positive.')

    @api.constrains('selling_price')
    def _check_price(self):
        for line in self:
            if line.selling_price<(line.expected_price*0.9) and line.selling_price>0:
                raise ValidationError("The pice is less than 90% of the expected price.")

    @api.constrains('expected_price')
    def _check_price2(self):
        for line in self:
            if line.selling_price<(line.expected_price*0.9) :
                line.offer_ids.status=''
                line.selling_price=0

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for res in self:
            b_price=res.mapped('offer_ids.price')
            # print("haaa",b_price)
            if b_price:
                res.best_price=max(b_price)
            else:
                res.best_price=0


    @api.depends('garden_area', 'living_area')
    def _compute_balance(self):
        for line in self:
            line.total = line.garden_area + line.living_area

    @api.onchange('garden')
    def onchange_garden(self):
        for line in self:
            if line.garden:
                line.garden_area=10
                line.garden_orientation='north'
            else:
                line.garden_area=0
                line.garden_orientation=''

    def sell(self):
        for record in self:
            if record.state!='cancelled':
                record.state='sold'
            else:
                raise UserError(('Cancelled properties cannot be sold.'))

        return True

    def cancel(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'cancelled'
            else:
                raise UserError(('Sold properties cannot be Cancelled.'))
        return True

    @api.ondelete(at_uninstall=True)
    def unlink_property(self):
        for record in self:
            # print("haaaa",self.state)
            if record.state in ['offer' ,'accepted','sold']:
                raise UserError(('Cancelled properties cannot be unlinked.'))





