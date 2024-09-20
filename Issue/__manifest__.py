{
    'name': "Issue",
    'version': '1.0',
    'depends': ['base','product','mrp','account','mail'],
    'author': "BWCS PMO",
    'category': 'Category',
    'license' : 'LGPL-3',
    'description': """
    Issue.问题单
    """,    
    'data': [
        'security/ir.model.access.csv',
        'views/issue_view.xml',
        'views/issue_code_view.xml',
        'views/issue_menus.xml',
        'data/issue_sequence.xml',  
        'data/issue_code_sequence.xml'  
    ]
}