{
    'name': 'Picking Operation Report',
    'version': '13.0.0.1',
    'category': 'Stock Picking',
    
    'summary': 'Modifictaion in standard stock picking Order reports',
    'description': "stock picking Order Report",
    'website': 'https://www.prixgen.com',
    'depends': ['web','purchase','base','account','stock'],
    'data': [ 
    'views/report_templates.xml',
    'views/picking_operation_report.xml',
     ],
    
    'installable': True,
    'application': True,
    'auto_install': False
}
