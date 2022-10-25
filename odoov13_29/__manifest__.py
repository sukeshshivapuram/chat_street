# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

{
    'name': 'Stock Transfer Order Change the state',
    'version': '13.1',
    'category': 'Inventory',
    'description': 'Allow To Confirm the Stock Tranfer Order  from the Tree View',
    'summary': 'Allow To Confirm the Stock Tranfer Order  from the Tree View',
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    # 'license': 'LGPL-3',
    'depends': [
         'odoov13_8'
    ],
    'data': [

        'wizards/stock_indent_view.xml',
    ],

    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
