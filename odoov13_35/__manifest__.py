# -*- coding: utf-8 -*-
{
    'name': 'MR Report',
    'version': '13.8',
    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'company':'Prixgen Tech Solutions Pvt. Ltd.',
    'website': "https://www.prixgen.com",
    'category': 'Inventory',
    'description': """
This module generates xlsx reports for MR	
""",
    'author': "Prixgen tech Solutions",
    'depends': ['stock'],
    'external_dependencies': {"python" : ["openpyxl"]},
    'data': [
        'wizard/mr_report_view.xml',
    ],
    'application': False,
    'installable': True,
}
