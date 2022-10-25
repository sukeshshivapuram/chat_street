# -*- coding: utf-8 -*-
{
    'name': 'To Detail Export Report',
    'version': '13.0.3',
    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': 'https://www.prixgen.com',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'category': 'Inventory',
    'description': """
This module generates xlsx reports for To Detail Export	
""",
    'depends': ['stock','odoov13_8','odoov13_43'],

    'data': [
        'wizard/to_detail_export_report_view.xml',
    ],
    'application': False,
    'installable': True,
}
