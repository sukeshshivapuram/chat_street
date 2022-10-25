# -*- coding: utf-8 -*-
{
    'name': 'Po Mismatch Report',
    'version': '13.0.2',
    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': 'https://www.prixgen.com',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'category': 'Inventory',
    'description': """
This module generates xlsx reports for Po Mismatch Records	
""",
    'depends': ['stock','odoov13_8'],

    'data': [
        'wizard/po_mismatch_report_view.xml',
    ],
    'application': False,
    'installable': True,
}
