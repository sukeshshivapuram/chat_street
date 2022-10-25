{
    'name': 'Curefit Barcode Print',
    'version': '13.0.0.1',
    'description': """Barcode Print for Curefit""",
    'category': 'Localization',
    'author': 'Prixgen Tech Solutions Pvt Ltd.',
    'company': 'Prixgen Tech Solutions Pvt Ltd.',
    'website': 'https://www.prixgen.com',
    'depends': ['base','stock','web','base_setup'],
    'data': [
        'reports/barcode_print_report.xml',
        'views/barcode_print_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
