import xmlrpc.client
# --- Odoo 18 (Source) ---
url_src = "http://localhost:8018"
db_src = "community_18"
user_src = "admin"
pwd_src = "admin"
common_src = xmlrpc.client.ServerProxy(f"{url_src}/xmlrpc/2/common")
uid_src = common_src.authenticate(db_src, user_src, pwd_src, {})
models_src = xmlrpc.client.ServerProxy(f"{url_src}/xmlrpc/2/object")
# --- Odoo 19 (Destination) ---
url_dest = "http://localhost:8019"
db_dest = "community_19"
user_dest = "admin"
pwd_dest = "admin"
common_dest = xmlrpc.client.ServerProxy(f"{url_dest}/xmlrpc/2/common")
uid_dest = common_dest.authenticate(db_dest, user_dest, pwd_dest, {})
models_dest = xmlrpc.client.ServerProxy(f"{url_dest}/xmlrpc/2/object")
# --- Fetch customers from Odoo 18 ---
partners_src = models_src.execute_kw(
    db_src, uid_src, pwd_src,
    'sale.order', 'search_read',
    [[]],
    {}
)
print(f"Fetched {len(partners_src)} customers from Odoo 18...")
# --- Transfer to Odoo 19 (Skip duplicates by email) ---
# created_count = 0
# skipped_count = 0
for orders in partners_src:
#     email = partner.get('email')
#     name = partner.get('name')
#     # Skip if email exists in Odoo 19
#     if email:
#         existing = models_dest.execute_kw(
#             db_dest, uid_dest, pwd_dest,
#             'res.partner', 'search',
#             [[('email', '=', email)]],
#             {'limit': 1}
#         )
#         if existing:
#             print(f"Skipped (duplicate email): {email}")
#             skipped_count += 1
#             continue
#     # Prepare minimal partner data
#     new_partner = {
#         'name': name or 'Unnamed',
#         'email': email,
#         'phone': partner.get('phone'),
#         'city': partner.get('city'),
#         'company_type': partner.get('company_type'),
#     }
    # Create in Odoo 19
    models_dest.execute_kw(
        db_dest, uid_dest, pwd_dest,
        'sale.order', 'create',
        [orders]
    )
#     created_count += 1
#     print(f"Created: {name}")
# print(f"\nCustomer transfer complete!")
# print(f"Created: {created_count}, Skipped: {skipped_count}")
