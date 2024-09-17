{
    'name': "Requirement & Evaluate",
    'version': '1.0',
    'author': "BWCS PMO",
    'category': 'Category',
    'license' : 'LGPL-3',
    'description': """
    Requirement & Evaluate 需求評估
    """,    
    'depends': ['base','product'],
    'data': [
        'security/ir.model.access.csv',
        'views/requirement_view.xml',
        'views/requirement_purpose_view.xml',
        'views/requirement_spec_view.xml',
        'views/requirement_menus.xml',
        'data/requirement_sequence.xml'     
    ]
}