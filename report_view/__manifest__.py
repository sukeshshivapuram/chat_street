{
    'name': " To get inventory transaction",
    'category': 'Inventory',
    'version': '13.0.10',
    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': 'https://www.prixgen.com',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'summary': 'Module to Balance Reset Reserve Quantity',
    'depends': ['base','product','stock','odoov13_47sh'],
    'data': [
        'security/ir.model.access.csv',       
        'views/unreserve_qty_view.xml', 
        # 'views/inv_report_view.xml',
        ], 
    'installable': True,
    'application': True,
}


