from odoo import http
from odoo import Command
from odoo.http import request

class MaterialRequestForm(http.Controller):
    @http.route('/website/request/view', type='http', auth='user', website=True)
    def request_view(self, **kw):
        requests = request.env['material.request'].search([])
        return request.render('material_request.request_list', {"requests": requests})

    @http.route('/website/request_view/views', type='http', auth='user', website=True)
    def request_wise_views(self, **kw):
        req_id = kw.get('req_id')

        requests = request.env['material.request'].search([('id', '=', req_id)])
        internal=False
        for data in  requests.request_line_ids:
            if data.request_type == 'internal':
                internal=True
        return request.render('material_request.req_detail_view', {"requests": requests, "internal": internal})

    @http.route('/website/request/form', type='http', auth='user', website=True)
    def request_form_view(self, **kw):
        products = request.env['product.product'].sudo().search([])
        customer = request.env['res.users'].sudo().search([])
        location = request.env['stock.location'].sudo().search([])
        datas = {
            'products': products,
            'customer': customer,
            'locations': location,
        }
        return request.render(
            'material_request.request_form_view', datas)

    @http.route('/material/submit', type='jsonrpc', auth='user', website=True)
    def request_submit(self, **post):
        name=post.get('req_name')
        date=post.get('date')
        lines = post.get('request_line_ids', [])
        formatted_lines = []

        for line in lines:
            line_vals = {
                'product_id': int(line.get('product_id')),
                'quantity': float(line.get('quantity')),
                'request_type': line.get('request_type'),
            }
            if line.get('request_type') == 'internal':
                if line.get('source_location_id'):
                    line_vals['source_location_id'] = int(line.get('source_location_id'))
                if line.get('destination_location_id'):
                    line_vals['destination_location_id'] = int(line.get('destination_location_id'))
            formatted_lines.append((0, 0, line_vals))
        request.env['material.request'].create({
            'req_name': name,
            'date': date,
            'request_line_ids': formatted_lines
        })
        requests = request.env['material.request'].search([])
        return request.render('material_request.request_list', {"requests": requests})

    @http.route('/website/request_send/views', type='http', auth='user', website=True)
    def request_wise_update(self, **kw):
        req_id = kw.get('req_id')
        requests = request.env['material.request'].search([('id', '=', req_id)])
        requests.write({'state' : 'submitted'})
        internal = False
        for data in  requests.request_line_ids:
            if data.request_type == 'internal':
                internal=True
        return (request.render('material_request.req_detail_view', {"requests": requests,"internal" : internal}))

    @http.route('/website/request_approve/views', type='http', auth='user', website=True)
    def request_wise_update_manager(self, **kw):
        req_id = kw.get('req_id')
        requests = request.env['material.request'].search([('id', '=', req_id)])
        requests.write({'state' : 'approved'})
        internal = False
        for data in  requests.request_line_ids:
            if data.request_type == 'internal':
                internal=True
        return request.render('material_request.req_detail_view', {"requests": requests,"internal" : internal})

    @http.route('/website/request_head/views', type='http', auth='user', website=True)
    def request_wise_update_head(self, **kw):
        req_id = kw.get('req_id')
        request.env['material.request'].action_head_approval_website(req_id)
        requests=request.env['material.request'].search([('id', '=', req_id)])
        internal = False
        for data in  requests.request_line_ids:
            if data.request_type == 'internal':
                internal=True
        return request.render('material_request.req_detail_view', {"requests": requests,"internal" : internal})

    @http.route('/website/request_head_cancel/views', type='http', auth='user', website=True)
    def request_wise_update_manager_cancel(self, **kw):
        req_id = kw.get('req_id')
        requests = request.env['material.request'].search([('id', '=', req_id)])
        requests.write({'state': 'reject'})
        internal = False
        for data in requests.request_line_ids:
            if data.request_type == 'internal':
                internal = True
        return request.render('material_request.req_detail_view', {"requests": requests, "internal": internal})