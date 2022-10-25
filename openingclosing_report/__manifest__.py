# -*- coding: utf-8 -*-
{
    'name': 'Stock Opening/Closing Report',
    'version': '13.4.1',
    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': 'https://www.prixgen.com',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'category': 'Inventory',
    'description': """
This module generates xlsx reports for Stock Opening/Closing
""",
    'depends': ['stock','odoov13_47sh'],

    'data': [
        'wizard/openclose_report.xml',
    ],
    'application': False,
    'installable': True,
}
