# -*- coding: utf-8 -*-
{
    "name": "Recurring Subscription",
    "version": "19.0.1.0.0",
    "sequence":"1",
    "author":"Cybrosys",
    "application": True,
    "depends": ['base','mail','crm','account','sale'],
    'data':[
        'security/recurring_subscription_groups.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/product_record.xml',
        'data/ir_cron_data.xml',
        'data/email_template.xml',
        'views/recurring_subscription_view.xml',
        'views/recurring_subscription_credit_view.xml',
        'views/recurring_subscription_billing_schedule_view.xml',
        'views/partner_account_id.xml',
        'views/res_partner_custom_field_view.xml',
        'views/crm_lead_field_view.xml',
        'views/subscription_credit_report_view.xml',
        'views/sale_order_view.xml',
        'views/subscription_report_wizard_view.xml',
        'report/subscription_report_pdf.xml',
        'report/subscription_report_template.xml',
        'report/credit_report_pdf.xml',
        'report/credit_report_template.xml',
        'report/ir_actions_report.xml',
        'report/subscription_report_action.xml',
        'report/credit_report_action.xml',
        'views/website_view.xml',
        'views/website_credit_view.xml',
        'views/website_billing_schedule.xml',
        'views/snippets/snippet_template.xml',

        'views/menu_list.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css',
            'recurring_subscription/s   tatic/src/js/select2.js',
            'recurring_subscription/static/src/js/credit_snippet.js',
            'recurring_subscription/static/src/xml/credit_snippet_template.xml',
        ],
        'web.assets_backend': [
            'recurring_subscription/static/src/js/action_manager.js',
        ],

    }

}
