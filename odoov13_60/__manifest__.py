{
    'name': 'Purchase Order Report',
    'version': '13.0.0.3',
    'category': 'Purchase',
    
    'summary': 'Modifictaion in standard Purchase Order reports',
    'description': "Purchase Order Report",
    'website': 'https://www.prixgen.com',
    'depends': ['web','purchase','base',],
    'data': [ 
    'views/report_templates.xml',
    'views/purchase_order_report.xml',
     ],
    
    'installable': True,
    'application': True,
    'auto_install': False
}
