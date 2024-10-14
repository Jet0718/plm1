{
    'name': 'project_inherit',
    'description': 'ebert DEV project_inherit',
    'author': 'BWCS PMO',
    'version': '1.0',
    'category': 'Uncategorized',
    'website': 'http://www.example.com',
    'depends': ['base','project','dms','plm_product'],
    'data': [
        'views/project_project.xml',
        'views/project_task.xml',
        'views/dms_file.xml', 
    ],
    'application': True,
}