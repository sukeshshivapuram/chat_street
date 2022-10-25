# -*- coding: utf-8 -*-
{
    'name': "Odoov13_18a",
    'summary':"""Purchase tolerance on products""",
    'description': """Tolerance for products can be added based on UOM to restrict the receipt of excess material""",
    'category': 'Test',
    'version': '13.0.9',
    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': 'https://www.prixgen.com',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    # 'description': """Purchase tolerence model""",
    # any module necessary for this one to work correctly
    'depends': ['base','account','product','stock',],

    # always loaded
    'data': [
             'views/purchase_tolerance_cf_view.xml',
             # 'models/purchase_tolerance_adithya.py',
    ],
}
