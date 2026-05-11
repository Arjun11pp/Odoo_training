import xmlrpc.client
# --- Odoo 18 (Source) ---
url_src = "http://localhost:8018"
db_src = "may8"
user_src = "1"
pwd_src = "1"
common_src = xmlrpc.client.ServerProxy(f"{url_src}/xmlrpc/2/common")
uid_src = common_src.authenticate(db_src, user_src, pwd_src, {})
models_src = xmlrpc.client.ServerProxy(f"{url_src}/xmlrpc/2/object")
# --- Odoo 19 (Destination) ---
url_dest = "http://localhost:8019"
db_dest = "test2"
user_dest = "1"
pwd_dest = "1"
common_dest = xmlrpc.client.ServerProxy(f"{url_dest}/xmlrpc/2/common")
uid_dest = common_dest.authenticate(db_dest, user_dest, pwd_dest, {})
models_dest = xmlrpc.client.ServerProxy(f"{url_dest}/xmlrpc/2/object")
# --- Fetch customers from Odoo 18 ---
sale_orders = models_src.execute_kw(
    db_src, uid_src, pwd_src, 'sale.order', 'search_read',  [[]],  {'fields':
        ['name', 'partner_id', 'date_order','state','company_id', 'user_id','payment_term_id','order_line','team_id','client_order_ref','picking_ids']}
)
print(f"Fetched {len(sale_orders)} customers from Odoo 18...")
# print(f"Fetched {(sale_orders)} customers from Odoo 18...")
# --- Transfer to Odoo 19 (Skip duplicates by email) ---
i=0
for orders in sale_orders:
    print('i', i)
    i += 1

    print('orders',orders)
    customer_id = orders['partner_id']
    name=customer_id[1]
    email = orders.get('email')
    existing = models_dest.execute_kw( db_dest, uid_dest, pwd_dest, 'res.partner', 'search', [[('name', '=', customer_id)]], {'limit': 1})

    if not existing:
        partner_details=models_src.execute_kw( db_src, uid_src, pwd_src,'res.partner', 'search_read',
            [[('id','=',customer_id[0])]], {'fields': ['name', 'email', 'phone','city']})
        existing = {
            'name': name or 'Unnamed',
            'email': partner_details[0].get('email'),
            'phone': partner_details[0].get('phone'),
            'city': partner_details[0].get('city'),
                }
        # models_dest.execute_kw(
        #     db_dest, uid_dest, pwd_dest,
        #     'res.partner', 'create',   [existing] )
        print('salesperson', orders.get('user_id')[0])
    # Create in Odoo 19
        user_details = models_src.execute_kw(db_src, uid_src, pwd_src,'res.users', 'search_read',
                                [[('id','=',orders.get('user_id')[0])]],{'fields': ['name', 'email', 'phone', 'city']})
        users = {
            'name': user_details[0].get('name'),
            'email': user_details[0].get('email'),
            'login': user_details[0].get('login'),
            'password': user_details[0].get('password'),
        }
    if order.get('picking_ids'):
        picking_ids = models_src.execute_kw(db_src, uid_src, pwd_src, 'sale.order.line', 'search_read',
                                            [[('id', '=', order.get('picking_ids'))]],
                                            {'fields': ['name', 'partner_id', 'picking_type_id', 'invoice_policy',
                                                        'schedule_date', 'date_deadline', 'origin', 'location_dest_id',
                                                        'location_id', 'move_type']})
        picking_details = {
            'picking_id': picking_ids[0].get('picking_id'),
            'picking_type_id': picking_ids[0].get('picking_type_id'),
            'invoice_policy': picking_ids[0].get('invoice_policy'),
            'schedule_date': picking_ids[0].get('schedule_date'),
            'date_deadline': picking_ids[0].get('date_deadline'),
            'origin': picking_ids[0].get('origin'),
            'location_dest_id': picking_ids[0].get('location_dest_id'),
            'location_id': picking_ids[0].get('location_id'),
            'move_type_id': picking_ids[0].get('move_type_id'),
        }
    order_details = {
        'partner_id': existing,
        'date_order': orders.get('date_order'),
        'state': orders.get('state'),
        'company_id': orders.get('company_id'),
        'picking_ids': picking_id,
        # 'user_id': user_details,
    }
    print('customer_id', existing)
    # user=models_dest.execute_kw(
    #     db_dest, uid_dest, pwd_dest,
    #     'res.user', 'create',
    #     [users],)

    # order_id= models_dest.execute_kw(
    #     db_dest, uid_dest, pwd_dest,
    #     'sale.order', 'create',
    #     [order_details])



        # picking_id= models_dest.execute_kw(
        #     db_dest, uid_dest, pwd_dest,'stock.picking', 'create', [picking_details])
    print('orderline', orders.get('order_line'))
    for lines in orders.get('order_line'):
        print('lines', lines)
        order_line = models_src.execute_kw(db_src, uid_src, pwd_src, 'sale.order.line','search_read',
                        [[('id','=',orders.get('user_id')[0])]],{'fields': ['name', 'product_id', 'product_uom_qty', 'price_unit' ,'order_id' ]})
        for lines2 in order_line:
            print('lines2', lines2)
            print('ll',lines2.get('product_id')[0])
            product_details = models_src.execute_kw(db_src, uid_src, pwd_src,'product.template', 'search_read',
                            [[('id','=',lines2.get('product_id')[0])]], {'fields': ['name', 'list_price','invoice_policy']})
            print('product', product_details)
            existing_product = models_dest.execute_kw(db_dest, uid_dest, pwd_dest,
                'product.template', 'search', [[('name', '=', product_details[0].get('name'))]], {'limit': 1})
            print('product_details', existing_product)
            if not existing_product:
                new_product = {
                    'name': product_details[0].get('name'),
                    'list_price': product_details[0].get('list_price'),
                    'invoice_policy': product_details[0].get('invoice_policy'),
                    }
                # existing_product=models_dest.execute_kw(db_dest, uid_dest, pwd_dest, 'product.product', 'create', [new_product])

            order_lines_details = {
                # 'product_id': pro,
                'product_uom_qty': product_details[0].get('product_uom_qty'),
                'price_unit': product_details[0].get('list_price'),
                # 'order_id': order_id,
                 }

            # sale_order_id = models_dest.execute_kw(db_dest, uid_dest, pwd_dest,
            #                     'sale.order.line', 'create',[order_lines_details])
#     created_count += 1
#     print(f"Created: {name}")
# print(f"\nCustomer transfer complete!")
# print(f"Created: {created_count}, Skipped: {skipped_count}")
