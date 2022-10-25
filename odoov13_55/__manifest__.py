# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Base Inventroy',
    'version': '13.4',
    'category': 'Products',
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'depends': ['base','stock', 'purchase','product','stock_account'],
    'description': """ Item category and product group code,
    Disallow negative stock levels by default,
    Product Category Filter""",
    'data': [
        'security/ir.model.access.csv',
        'views/item_category_view.xml',
        'views/product_category_secondary_view.xml',
        'views/product_group_primary_view.xml',
        # 'views/item_view.xml',
        
    ],
    
    'installable': True,
    'auto_install': False,
}
