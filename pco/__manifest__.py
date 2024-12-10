{
    'name': "PCO",
    'version': '1.0',
    'depends': ['base','plm_product','mrp','plm','project_inherit'],
    'author': "BWCS PMO",
    'category': 'Category',
    'license' : 'LGPL-3',
    'description': """
    PCO 产品签审单 
    """,    
    'data': [
        'security/ir.model.access.csv',
        'demo/pco_type.xml',
        'views/pco_view.xml',
        'views/pco_tag_view.xml',
        'views/pco_product_view.xml', 
        'views/pco_bom_view.xml',        
        'views/pco_type_view.xml',
        'views/pco_menus.xml',
        'data/pco_sequence.xml'     
    ],
    'demo': [
        "demo/pco_type.xml",       
    ],
}