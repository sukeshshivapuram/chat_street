# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Odoov13_7a',
    'version': '13.2',
    'category': 'Sales/Inventory',
    'summary': 'In Inventory filter the record the based on the Resposible Users',
    'description': """
This module for record rules .
    """,
    'depends': [ 'sale','sale_stock','stock'],
    'data': [
        
        'security/sale_data.xml',
        'views/sale_views.xml',
    ],
   
    'installable': True,
    'auto_install': False
}
