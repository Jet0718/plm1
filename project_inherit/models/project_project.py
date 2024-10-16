from odoo import api,fields, models,_

class InhtProjectModel(models.Model):
    _inherit = "project.project"    

    cn_prj2pdt_ship = fields.Many2one('product.template', string= '产品')
    dmsfile_ids = fields.One2many('dms.file','cn_file2prj')
    dmsfile_count =fields.Integer("数量" ,compute='_compute_dmsfile_count')

    #计算关联dmsfile的数量
    @api.depends("dmsfile_ids")
    def _compute_dmsfile_count(self):
        for record in self:
            record.dmsfile_count = len(record.dmsfile_ids)
    #按钮开启反查页面        
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
    
    
    

    

