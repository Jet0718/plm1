{
    'name': 'project_inherit',
    'description': 'ebert DEV project_inherit',
    'author': 'BWCS PMO',
    'version': '1.0',
    'license': 'LGPL-3',
    'category': 'Uncategorized',
    'website': 'http://www.example.com',
    'depends': ['base','project','plm_product','plm'],
    'data': [               
        'data/irattachmen_seq.xml', 
        'views/project_project.xml',
        'views/project_task.xml',
        'views/ir_attachment_view.xml',
        'views/ir_attachment_relations.xml', 
    ],
    'application': True,
}