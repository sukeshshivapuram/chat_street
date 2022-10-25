{
    # App information
    'name': 'Patch 8',
    'version': '13.0.2.23',
    'category': 'Operations/Inventory',
    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': 'https://www.prixgen.com',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'summary' : 'Manages Inter Company and Inter Warehouse Transfer.', 
    'description':"""
        Module to manage Inter Company Transfer and Inter Warehouse Transfer along with all required documents with easiest way by just simple configurations.
        """,


    # Dependencies
    'depends': ['base','purchase_stock', 'barcodes',],
    'data': [
        'data/ir_sequence.xml',
        'data/inter_company_transfer_config.xml',

        'views/inter_company_transfer_ept.xml',
        'views/inter_company_transfer_config_ept.xml',
        'views/res_company.xml',
        # 'views/sale.xml',
        'views/purchase.xml',
        'views/stock_picking.xml',
        'views/account_move.xml',
        'views/inter_company_transfer_log_book_ept.xml',
        'views/stofields.xml',

        'security/inter_company_transfer_security.xml',
        'security/ir.model.access.csv',

        'wizards/reverse_inter_company_transfer_ept.xml',
        'wizards/import_export_products_ept.xml',

        ],

  
    'post_init_hook': 'post_init_update_rule',
    'uninstall_hook': 'uninstall_hook_update_rule',
    'active': True,
    'installable': True,
    'auto_install': False,
    'application': True,
}
