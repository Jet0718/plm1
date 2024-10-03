{
    'name': 'cn_plm_product',
    'description': 'ebert plm_product',
    'author': 'BWCS PMO',
    'version': '1.0',
    'category': 'Uncategorized',
    'license' : 'LGPL-3',
    'website': 'http://www.openplm.com.tw',
    'depends': ['base','mrp'],
    'data': [
        'views/product_templates.xml',
        'views/mrp_bom_views.xml',
        'data/prodcut_sequence.xml',
        'data/prodbom_sequence.xml',        
        'security/ir.model.access.csv',       
    ],
    'application': True,
}