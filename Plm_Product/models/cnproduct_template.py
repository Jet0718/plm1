from odoo import api,fields, models,_

class InhtProductModel(models.Model):
    _inherit = "product.template"

    item_number = fields.Char(string="編號",default=lambda self:_("no"),copy=False,readonly=True)
    xspec       = fields.One2many('product.spec', 'prd_id', '規格特性')
    state = fields.Selection([
            ('Draft', 'Draft'),
            ('Review', 'Review'),
            ('Released', 'Released'),
            ('InChange', 'InChange'),
            ('Superseded', 'Superseded')],string = "狀態",
            copy=False, default='Draft', readonly=True, required=True, index=True)

    #ebert         
    #cn_is_current = fields.Boolean('is Current', default=True)
    cnis_current = fields.Boolean('isCurrent', default=True,readonly=True)
    cn_configid = fields.Char(string='configid',default="0",copy=False,readonly=True)
    
    pdt2pdt_id = fields.Many2one(
        'product.template', 'product_template',
        ondelete='cascade', required=False)
    cn_pdt2version_ship = fields.One2many('product.template', 'pdt2pdt_id', '历程记录')
    version=fields.Integer("version",default=1,copy=False,readonly=True)



    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            if vals.get('item_number',_('no'))== _('no'):
                vals['item_number'] =self.env['ir.sequence'].next_by_code('product.templat')               
               # super().create(vals_list)
                res = super(InhtProductModel, self).create(vals_list)
                if  res.cn_configid =="0"  :
                    res.write({'cn_configid': res.id})
                return res


            
             

            #ebert add set config_id
            # if  self.cn_configid !="0"  :
            #     self.write({'cn_configid': self.id})
         
    #ebert按钮跳转页面    
    def action_open_versions(self): 
         return {
            'name': '历程记录',
            'res_model': 'product.template', 
            'view_mode': 'tree,form',
            #'view_id': self.env.ref('product.template.product_template_tree_view').id,   
            'domain': [('active', '=', False),('cn_configid', '=', self.cn_configid)],  
            #'context': {'search_default_group': 'my_group'},
            'type': 'ir.actions.act_window',
        }

class productSpec(models.Model):
    _name="product.spec"
    _description="Specification for Part"

    prd_id=fields.Many2one('product.template',"product",required=True)

    name = fields.Char(string="規格名稱")
    description= fields.Char(string="內容")
