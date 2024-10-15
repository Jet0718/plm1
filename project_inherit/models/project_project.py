from odoo import api,fields, models,_

class InhtProjectModel(models.Model):
    _inherit = "project.project"    
<<<<<<< HEAD

    cn_prj2pdt_ship = fields.Many2one('product.template', string= '产品')
    dmsfile_ids = fields.One2many('dms.file','cn_file2prj')
    dmsfile_count =fields.Integer("数量" ,compute='_compute_dmsfile_count')

    #计算关联dmsfile的数量
    @api.depends("dmsfile_ids")
    def _compute_dmsfile_count(self):
        for record in self:
            record.dmsfile_count = len(record.dmsfile_ids)
    #按钮开启反查页面        
=======
    
    # project2pdt_id = fields.Many2one(
    #     'product.template', 'product_template',
    #     ondelete='cascade', required=False)
    # cn_project2pdt_ship = fields.Many2one('product.template', 'producnt', '项目文件')
    cn_prj2pdt_ship = fields.Many2one('product.template', string= '产品')
    #cn_prj2file = fields.Many2one('dms.file', string= 'file')
    # cn_prj2file1 = fields.Many2one('dms.file', string= 'file')

>>>>>>> dbc8a95025e00e02717bd9748717216622145e8e
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
    
<<<<<<< HEAD
    
=======
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
>>>>>>> dbc8a95025e00e02717bd9748717216622145e8e
    

    

