{
    'name': "Issue",
    'version': '1.0',
    # 2024.9.25 Herbert新增内容:引用project,DCO,PCO 
    'depends': ['base','product','mrp','account','mail','project','pco','dco'],
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
        'views/issue_pco_view.xml',
        'views/issue_dco_view.xml',
        'views/issue_product_view.xml',
        'views/issue_project_view.xml',
        'data/issue_sequence.xml',  
        'data/issue_code_sequence.xml'  
    ]
}