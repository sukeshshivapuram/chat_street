# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

{
    'name': 'Material Indent Change the state',
    'version': '13.3',
    'category': 'Inventory',
    'description': 'Allow To Confirm the Material Indent  from the Tree View',
    'summary': 'Allow To Confirm the Material Indent  from the Tree View',
    'author': 'Prixgen Tech Solutions Pvt Ltd',
    'maintainer': 'Prixgen Tech Solutions Pvt Ltd',
    'support': 'https://www.prixgen.com',
    'website': 'https://www.prixgen.com',
    # 'license': 'LGPL-3',
    'depends': [
         'odoov13_15','odoov13_16','odoov13_9'
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
