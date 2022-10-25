{
    'name': 'Odoov13_12sha',
    'version': '13.0.0.10',
    'description': """Delivery Slip Report for Curefit""",
    'category': 'Localization',
    'author': 'Prixgen Tech Solutions Pvt Ltd.',
    'company': 'Prixgen Tech Solutions Pvt Ltd.',
    'website': 'https://www.prixgen.com',
    'depends': ['base','stock','product'],
    'data': [
        'reports/delivery_slip_report.xml',
        'views/delivery_slip_template.xml',
        'views/delivery_slip_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
