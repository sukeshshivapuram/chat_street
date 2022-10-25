{
    'name': 'Odoov13_6a',
    'version': '13.0.0.11',
    'category': 'Operations/Inventory',
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'depends': ['stock','stock_barcode','web_tour','web','stock_barcode_mobile'],
    'data': [
        'views/assets.xml',
        'views/stock_picking.xml',
        
    ],
    'qweb': [
        "static/src/xml/putaway_button.xml",
        
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
