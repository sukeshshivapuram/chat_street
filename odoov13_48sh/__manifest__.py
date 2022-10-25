# -*- coding: utf-8 -*-
{
    'name': 'Purchase Receipt Date',
    'version': '13.0.2.0.0',
    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': 'https://www.prixgen.com',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'license': 'OPL-1',
    'category': 'Tools',
    'summary': 'Purchase Receipt Date',
    'description': """
Purchase Receipt Date
---------------------

Purchase Receipt Date
""",
    'depends': ['purchase', 'stock'],
    'data': [
        'data/purchase_cron.xml',
    ],
    'installable': True,
    'auto_install': False,
}
