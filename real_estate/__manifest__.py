{
    "name": "Real Estate",
    "application": True,
    "depends": ["base","sale"],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',


        'views/estate_action.xml',

        'views/estate_property_views.xml'


    ],
    'license': 'LGPL-3',

}
