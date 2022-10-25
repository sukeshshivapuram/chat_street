# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Price List City Wise',
    'version': '13.0.2.6',
    'category': 'purchase',
    'summary': 'Mapping the city with warehouse get the price list base on the vendore.',
    'description': """
Price List .
    """,
    'depends': ['stock','purchase','purchase_stock'],
    'data': [
        
        'security/ir.model.access.csv',
        'views/price_list_view.xml',
    ],
   
    'installable': True,
    'auto_install': False
}
