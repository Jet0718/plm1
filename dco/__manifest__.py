{
    'name': "DCO",
    'version': '1.0',
    'depends': ['base','product','mrp','project_inherit','plm', "base_tier_validation"],
    'author': "BWCS PMO",
    'category': 'Category',
    'license' : 'LGPL-3',
    'description': """
    DCO 图文签审单
    """,    
    'data': [
        'security/ir.model.access.csv',
        'views/dco_view.xml',
        'views/dco_tag_view.xml',
        'views/dco_menus.xml',
        'views/dco_file_view.xml',
        'data/dco_sequence.xml'     
    ]
}