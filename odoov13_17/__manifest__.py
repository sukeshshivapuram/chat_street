# -*- coding: utf-8 -*-
{
    'name': 'Odoov13_17a',
    'version': '13.0.1.2',
    'category': 'Customization',
    'description': u"""
This model aggrigates inventory
""",
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'depends': [
        'base',
        'product',
        'purchase',
    ],
    'data': [
        'views/views.xml',
        'security/ir.model.access.csv',
    ],
    'application': False,
    'installable': True,
}
