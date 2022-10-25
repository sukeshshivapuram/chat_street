# -*- coding: utf-8 -*-
{
    'name': 'odoov13_9',
    'version': '13.0.1.10',
    'category': 'Customization',
    'description': """Prix
This model aggrigates inventory
""",
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'depends': [
        'base',
        'product',
        'stock',
        'purchase',
        'purchase_stock',
        'odoov13_4'
    ],
    'data': [
        'views/views.xml',
        'security/ir.model.access.csv',
    ],
    'application': False,
    'installable': True,
}
