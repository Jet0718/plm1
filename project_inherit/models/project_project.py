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

    def open_dmsfile_btn(self):
        return {
            'name': '项目关联文件',
            'res_model': 'dms.file', 
            'view_mode': 'tree,form',
            #'view_id': self.env.ref('product.template.product_template_tree_view').id,   
            'domain': [('active', '=', True),('cn_file2prj', '=', self.id)],  
            #'context': {'search_default_group': 'my_group'},
            'create' :False,
            'type': 'ir.actions.act_window',
        }
    
    # def issue_model_action(self):
    #     # raise UserError('已是"审核中"状态'+self.id)
    #     return {
    #         'name': '关联Issu',
    #         'res_model': 'issue', 
    #         'view_mode': 'tree,form',
    #         #'view_id': self.env.ref('product.template.product_template_tree_view').id,   
    #         'domain': [("project_id", "=", self.id)],  
    #         #'context': {'search_default_group': 'my_group'},
    #         'type': 'ir.actions.act_window',
    #     }
    

    

