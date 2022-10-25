# -*- coding: utf-8 -*-
{
    'name': 'Purchase Report',
    'version': '13.3',
    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': 'https://www.prixgen.com',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'category': 'Purchase',
    'description': """
This module generates xlsx reports for Purchase Report	
""",
    'depends': ['purchase'],

    'data': [
        'wizard/purchase_report_view.xml',
    ],
    'application': False,
    'installable': True,
}
