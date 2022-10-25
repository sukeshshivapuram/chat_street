# -*- coding: utf-8 -*-
{
    'name': 'Curefit API Integration Patch',
    'version': '13.0.3.6',
    'category': 'Customization',
    'description': u"""
This model aggrigates inventory
""",
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'depends': [
        'base',
        'product',
        'stock',
        'odoov13_4',
        'odoov13_50'
    ],
    'data': [
        'views/views.xml',
        'security/ir.model.access.csv',
    ],
    'application': False,
    'installable': True,
}
