from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request


class WebsiteCustomerForm(http.Controller):
    @http.route('/website/subscriptions/view', type='http', auth='public', website=True)
    def subscription_view(self, **kw):
        """Render the customer creation form"""

        subscriptions = request.env['recurring.subscription'].search([])
        return request.render('recurring_subscription.subscription_list',{"subscriptions":subscriptions})

    @http.route('/website/subscription/form', type='http', auth='public', website=True)
    def customer_form(self, **kw):
        """Render the customer creation form"""
        products = request.env['product.product'].sudo().search([])
        customers = request.env['res.partner'].sudo().search([('establishment_id' , '!=', False) ])
        return request.render('recurring_subscription.customer_form_template',{'products': products ,"customers" : customers})

    @http.route('/website/credit/form', type='http', auth='public', website=True)
    def credit_form(self, **kw):
        """Render the customer creation form"""
        subscriptions = request.env['recurring.subscription'].search([])
        return request.render('recurring_subscription.credit_form_template',
                              {'subscriptions': subscriptions})

    @http.route('/website/credit/create', type='http', auth='public', methods=['POST'], website=True, csrf=True)
    def create_credit(self, **post):
        name = post.get('sub_id')
        amount = post.get('amount')
        date=post.get('date')
        request.env['recurring.subscription.credit'].sudo().create({
            'recurring_subscription_id': name,
            'period_date': date,
            'credit_amount': amount,

        })

        return request.render('recurring_subscription.credit_success_template')

    @http.route('/website/credit/view', type='http', auth='public', website=True)
    def credit_view(self, **kw):
        """Render the customer creation form"""
        subscriptions = request.env['recurring.subscription.credit'].search([])
        return request.render('recurring_subscription.credit_list', {"subscriptions": subscriptions})

    @http.route('/website/unique_subscriptions/views/<int:sub_id>', type='http', auth='public', website=True)
    def unique_view(self,  sub_id,**kw):
        """Render the customer creation form"""
        print('123',sub_id)
        subscriptions = request.env['recurring.subscription.credit'].search([])
        return request.render('recurring_subscription.credit_list', {"subscriptions": subscriptions})

    # @http.route('/website/subscription/single_view', type='http', auth='public', methods=['POST'], website=True)
    # def subscription_view(self, **post):
    #     """Render the customer creation form"""
    #     sub=post.get('sub')
    #     print(sub)
    #     subscriptions = request.env['recurring.subscription'].search([])
    #     return request.render('recurring_subscription.subscription_list', {"subscriptions": subscriptions})

    @http.route('/website/subscription/create', type='http', auth='public', methods=['POST'], website=True, csrf=True)
    def create_customer(self, **post):
        """Handle form submission and create a new customer"""
        name = post.get('name')
        customer = post.get('customer_id')

        products= post.get('product_id')
        amount = post.get('amount')

        partner = self.env['res.partner'].search([('id', '=', customer)])
        print(partner)
        if not name:
            print('111')
            return request.render('recurring_subscription.customer_form_template', {
                'error': 'Name is required!'
            })
        if partner:
            establishment= partner.establishment_id
            if not establishment:
                print(establishment)
                return {
                    'success': False,
                    'message': 'This is a warning message from the controller!'
                }


        else:
            raise ValidationError('the selected customer has no Establishment ID !')

        request.env['recurring.subscription'].sudo().create({
            'name': name,
            'establishment': establishment ,

            'product_id': products,
            'customer_id': customer,
            'recurring_amount': amount,

        })
        # print('123')
        return request.render('recurring_subscription.customer_success_template')

    # @http.route('/website/unique_subscriptions/views', type='http', auth='public', website=True)
    # def subscription_unique_view(self, **kw):
    #     """Render the customer creation form"""
    #     print("122",sub_id)
        # subscriptions = request.env['recurring.subscription'].search([])
        # return request.render('recurring_subscription.subscription_list', {"subscriptions": subscriptions})

    @http.route('/website/billing/form', type='http', auth='public', website=True)
    def subscription_billing_form(self, **kw):
        """Render the customer creation form"""

        subscriptions = request.env['recurring.subscription'].search([])
        return request.render('recurring_subscription.billing_form_template', {"subscriptions": subscriptions})

    @http.route('/website/billing/view', type='http', auth='public', website=True )
    def subscription_billing_view(self, **kw):
        """Render the customer creation form"""
        billing = request.env['billing.schedule'].search([])
        return request.render('recurring_subscription.billing_list', {"billing": billing})

    @http.route('/website/billings/create', type='http', auth='public', methods=['POST'], website=True)
    def subscription_billing_create(self, **post):
        """Render the customer creation form"""
        name = post.get('name')

        sub_id = request.httprequest.form.getlist('sub_ids')
        print(type(sub_id))
        print("121",sub_id)
        sub_ids=[int(i) for i in sub_id]
        print(sub_ids)
        # request.env['billing.schedule'].sudo().create({
        #     'name': name,
        #     'recurring_subscription_ids': sub_ids,
        # })
        request.env['billing.schedule'].test_fun()

        return request.render('recurring_subscription.billing_success_template')
