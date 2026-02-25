from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

class WebsiteCustomerForm(http.Controller):

    # Subscription page
    @http.route('/website/subscriptions/view', type='http', auth='public', website=True)
    def subscription_view(self, **kw):
        subscriptions = request.env['recurring.subscription'].search([])
        return request.render('recurring_subscription.subscription_list',{"subscriptions":subscriptions})

    @http.route('/website/subscription/form', type='http', auth='public', website=True)
    def customer_form(self, **kw):
        products = request.env['product.product'].search([])
        customers = request.env['res.partner'].search([('establishment_id' , '!=', False) ])
        return (request.render('recurring_subscription.customer_form_template',{'products': products ,"customers" : customers}) )

    @http.route('/website/unique_subscriptions/views', type='http', auth='public', website=True)
    def unique_view(self,  **kw):
        sub_id=kw.get('sub_id')
        subscriptions = request.env['recurring.subscription'].search([('id', '=', sub_id)])
        return request.render('recurring_subscription.subscription_detail_view', {"subscription": subscriptions})

    @http.route('/website/confirm_subscription/views', type='http', auth='public', website=True)
    def confirm_subscription(self, **kw):
        sub_id = kw.get('sub_id')
        subscriptions = request.env['recurring.subscription'].search([('id', '=', sub_id)])
        subscriptions.write({'state' : 'confirm'})
        return request.render('recurring_subscription.subscription_detail_view', {"subscription": subscriptions})

    @http.route('/website/subscription/create', type='http', auth='public', methods=['POST'], website=True, csrf=True)
    def create_customer(self, **post):
        name = post.get('name')
        customer = post.get('customer_id')
        products = post.get('product_id')
        amount = post.get('amount')
        partner = request.env['res.partner'].search([('id', '=', customer)])
        if partner:
            establishment = partner.establishment_id
            if not establishment:
                return {
                    'success': False,
                    'message': 'This is a warning message from the controller!'}
        else:
            raise ValidationError('the selected customer has no Establishment ID !')
        request.env['recurring.subscription'].create({
            'name': name,
            'establishment': establishment,
            'product_id': products,
            'customer_id': customer,
            'recurring_amount': amount,
        })
        # subscriptions = request.env['recurring.subscription'].search([])
        return request.redirect('/website/subscriptions/view')

    # Credit Page

    @http.route('/website/credit/form', type='http', auth='public', website=True)
    def credit_form(self, **kw):
        subscriptions = request.env['recurring.subscription'].search([])
        return request.render('recurring_subscription.credit_form_template',{'subscriptions': subscriptions})

    @http.route('/website/credit/create', type='http', auth='public', methods=['POST'], website=True, csrf=True)
    def create_credit(self, **post):
        name = post.get('sub_id')
        amount = post.get('amount')
        date=post.get('date')
        sub=request.env['recurring.subscription'].search([('id', '=', name)]).recurring_amount
        if int(amount) > sub:
            print('111')
            warning_message = "amount is greater than the subscription amount!"
            subscriptions = request.env['recurring.subscription'].search([])
            return request.render('recurring_subscription.credit_form_template', {
                'warning_message': warning_message,'subscriptions': subscriptions
            })
        else:
            request.env['recurring.subscription.credit'].create({
                'recurring_subscription_id': name,
                'period_date': date,
                'credit_amount': amount,
            })
        return request.redirect('/website/credit/view')

    @http.route('/check_condition', type='http', auth='public',website=True)
    def my_handler(self, **post):
        return http.request.render('recurring_subscription.credit_list', {
            'warning_msg': "Something went wrong!"
        })

    @http.route('/website/credit/view', type='http', auth='public', website=True)
    def credit_view(self, **kw):
        subscriptions = request.env['recurring.subscription.credit'].search([])
        return request.render('recurring_subscription.credit_list', {"subscriptions": subscriptions})

    @http.route('/website/approve_credit/views', type='http', auth='public', website=True)
    def approve_credit(self, **kw):
        sub_id = kw.get('sub_id')
        credit = request.env['recurring.subscription.credit'].search([('id', '=', sub_id)])
        credit.write({'state': 'approved'})
        return request.render('recurring_subscription.credit_detail_view', {"credit": credit})

    @http.route('/website/unique_credit/views', type='http', auth='public', website=True)
    def unique_credit_view(self,  **kw):
        sub_id=kw.get('sub_id')
        credit = request.env['recurring.subscription.credit'].search([('id', '=', sub_id)])
        return request.render('recurring_subscription.credit_detail_view', {"credit": credit})

    # Billing page

    @http.route('/website/billing/form', type='http', auth='public', website=True)
    def subscription_billing_form(self, **kw):
        subscriptions = request.env['recurring.subscription'].search([('state','=','confirm')])
        return request.render('recurring_subscription.billing_form_template', {"subscriptions": subscriptions})

    @http.route('/website/billing/view', type='http', auth='public', website=True )
    def subscription_billing_view(self, **kw):
        billing = request.env['billing.schedule'].search([])
        return request.render('recurring_subscription.billing_list', {"billing": billing})

    @http.route('/website/billings/create', type='http', auth='public', methods=['POST'], website=True)
    def subscription_billing_create(self, **post):
        name = post.get('name')
        sub_id = request.httprequest.form.getlist('sub_ids')
        sub_ids=[int(i) for i in sub_id]
        period=post.get('period')
        request.env['billing.schedule'].create({
            'name': name,
            'recurring_subscription_ids': sub_ids,
            'period':period
        })
        return request.redirect('/website/billing/view')

    @http.route('/website/unique_billing/views', type='http', auth='public', website=True)
    def unique_billing_view(self, **kw):
        bill_id = kw.get('bill_id')
        bill = request.env['billing.schedule'].search([('id', '=', bill_id)])
        return request.render('recurring_subscription.billing_detail_view', {"bill": bill})

    @http.route('/website/billing_create_invoice/views', type='http', auth='public', website=True)
    def billing_create_invoice(self, **kw):
        bill_id = kw.get('bill_id')
        request.env['billing.schedule'].action_create_billing_invoice_website(bill_id)
        return request.render('recurring_subscription.billing_invoice_success')



    @http.route('/get_credit_list', auth="public", type='jsonrpc', website=True)
    def get_product_category(self):
        partner = request.env.user.partner_id
        credits_ids = request.env['recurring.subscription.credit'].search_read([('partner_id', '=', partner.id)], fields=['id', 'recurring_subscription_id', 'partner_id',
                    'credit_amount', 'state', 'credit_image'], order='id DESC' )
        return {
            'credits_ids': credits_ids,
        }

    @http.route('/get_credit_detail/<int:credit_id>', auth="public", type='http', website=True)
    def view_credit_detail(self,credit_id, **kw):
        credit_details=request.env['recurring.subscription.credit'].search([('id', '=', credit_id)])
        return request.render('recurring_subscription.credit_detail_view', {"credit": credit_details})

