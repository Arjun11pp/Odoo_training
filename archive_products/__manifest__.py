# -*- coding: utf-8 -*-
{
    "name": "Archive products",
    "depends": ["base","sale",'purchase','project'],
    "application": True,
    "installable": True,
    "sequence": "2",
    'data': [
        'security/record_rule.xml',
        'views/product_product_view.xml',
        'views/project_task_view.xml',
        'data/ir_cron_data.xml',
        'views/reference_field_view.xml',
        'views/purchase_order_view.xml',
        'views/res_user_view.xml',
        'data/delivery_product.xml'
    ]
}