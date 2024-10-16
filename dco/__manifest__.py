{
    'name': "DCO",
    'version': '1.0',
    'depends': ['base','product','mrp','project_inherit'],
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
        'data/dco_sequence.xml'     
    ]
}