# -*- coding: utf-8 -*-
{
    'name': 'For loss reason in the inventory adjustments',
    'version': '13.0.2.0.0',
    'author': 'Prixgen Tech Solutions Pvt.Ltd.',
    'website': 'https://wwww.prixgen.com',
    'company': 'Prixgen Tech Solutions Pvt.Ltd.',
    'license': 'OPL-1',
    'category': 'Iventory',
    'summary': 'Add new field loss reason in the inventory adjustments',
    'description': """Loss reason
""",
    'depends': ['stock'],
    'data': [
        'views/inventory_view.xml',
        'views/templates.xml',
        'wizard/grrtv_report_wizard.xml',
    ],
    'installable': True,
    'auto_install': False,
}
