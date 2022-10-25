{
    'name': 'Portal Vendor Management',
    'version': '13.0.0.12',
    'category': 'web',
    'author': 'Prixgen Tech Solutions Pvt. Ltd.',
    'company':  'Prixgen Tech Solutions Pvt. Ltd.',
    'website': 'https://www.prixgen.com',
    'depends': ['web','purchase','website','stock','odoov13_9','portal','utm','odoov13_13'],
    'data': [
        'views/assets.xml',
        'views/purchase_order_view.xml',
        'views/stock_picking.xml',
        'views/purchase_order_web.xml',
        
    ],
    'qweb': [

    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}