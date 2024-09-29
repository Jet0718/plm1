from odoo import api,fields, models,_

class InhtProjectModel(models.Model):
    _inherit = "project.project"    
    
    # project2pdt_id = fields.Many2one(
    #     'product.template', 'product_template',
    #     ondelete='cascade', required=False)
    # cn_project2pdt_ship = fields.Many2one('product.template', 'producnt', '项目文件')
    cn_prj2pdt_ship = fields.Many2one('product.template', string= '产品')
    #cn_prj2file = fields.Many2one('dms.file', string= 'file')

    # cn_prj2file1 = fields.Many2one('dms.file', string= 'file')
    

    

