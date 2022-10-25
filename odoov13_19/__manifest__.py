# -*- coding: utf-8 -*-
{
    'name': 'Odoo13_19a',
    'version': '13.0.2.0',
    'category': 'Customization',
    'description': u"""
This model prints specified number of barcodes for a selected sequence
""",
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'depends': [
        'base',
        'web',
        'base_setup',
        'odoov13_21',
    ],
    'data': [
        'views/views.xml',
        'security/ir.model.access.csv',
    ],
    'application': False,
    'installable': True,
}
