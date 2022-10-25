# -*- coding: utf-8 -*-
{
    'name': 'Gr Mismatch Report',
    'version': '13.2',
    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': 'https://www.prixgen.com',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'category': 'Inventory',
    'description': """
This module generates xlsx reports for To-Gr Mismatch	
""",
    'depends': ['stock','odoov13_8'],

    'data': [
        'wizard/gr_mismatch_report_view.xml',
    ],
    'application': False,
    'installable': True,
}
