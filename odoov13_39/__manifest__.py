# -*- coding: utf-8 -*-
{
    'name': 'Stock Adjustment Report',
    'version': '13.3',
    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'category': 'Inventory',
    'description': """
This module generates xlsx reports for Stock Adjustment	
""",
    'author': "Prixgen tech Solutions",
    'depends': ['stock','odoov13_42sh'],

    'data': [
        'wizard/stock_report_view.xml',
    ],
    'application': False,
    'installable': True,
}
