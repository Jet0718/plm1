from odoo import api,fields, models,_
from datetime import timedelta
from odoo.exceptions import UserError

class PCOModel(models.Model):
    _name = "pco"
    _description = "PCO main model for OpenPLM."
    _inherit = ['mail.thread','mail.activity.mixin']
        
    item_number =fields.Char("編號" , default=lambda self: _('New'), copy=False , readonly=True )
    title=fields.Char("主旨" ,compute='_compute_c',required=True,readonly=False,default=" ") 
    description=fields.Char("說明")
    flow_class =fields.Selection(
        string="審批類別",
        selection=[('Product','产品'),('Bom','物料清单')],
        required=True
    )
    owner_id =fields.Many2one('res.users',string='責任人',default=lambda self: self.env.user)
    contactor_id =fields.Many2one('res.users',string='核決者',required=True)  
    tag_ids = fields.Many2many('pco.tag', string='Tags')
    state =fields.Selection(
        string="状态",
        selection=[('New','草稿'),('Review','审核中'),('Approved','核准'),('Cancel','取消')],
        default="New",readonly=True,tracking=1
    )
    affected_product_id =fields.Many2one('product.template',string='審批产品')
    product_name =fields.Char("产品名称" ,related ='affected_product_id.name')   #抄写某模型中的某个栏位
    affected_bom_id =fields.Many2one('mrp.bom',string='审批物料清单') 
    active =fields.Boolean("啟用",default=True)    

    #ebert 
    new_affected_bom_id =fields.Many2one('mrp.bom',string='新版物料清单')
    new_affected_product_id =fields.Many2one('product.template',string='新版審批产品')  
    #添加显示版本
    affected_product_version = fields.Integer('产品旧版本',  related='affected_product_id.version', readonly=True)
    affected_bom_version = fields.Integer('物料清单旧版本',  related='affected_bom_id.version', readonly=True)
    new_affected_product_version = fields.Integer('产品新版本',  related='new_affected_product_id.version', readonly=True)
    new_affected_bom_version = fields.Integer('物料清单新版本',  related='new_affected_bom_id.version', readonly=True)
    #ebert end 

    # #上传单个档案写法
    # binary_field = fields.Binary("档案")
    # binary_file_name =fields.Char("档案名称")
    # #上传多个档案写法
    binary_fields =fields.Many2many("dms.file",string="Multi Files Upload")

    # Seqence 自动领号写法
    @api.model_create_multi
    def create(self, vals_list):
         """ Create a sequence for the requirement model """
         for vals in vals_list:
               if vals.get('item_number', _('New')) == _('New'):
                      vals['item_number'] = self.env['ir.sequence'].next_by_code('pco')
                      return super().create(vals_list)     
    
    #定义按钮
    def action_set_Review(self):
        if self.state =='New':
            self.write ({'state':'Review'})  
            
            #ebert version item 换版 条件判断送审物件的版本是否是1， 是则送审发布，否则换版
            if self.flow_class =='Product':
                
                if self.affected_product_id.version !=1  or self.affected_product_id.state == 'Released':
                    copyitem=self.affected_product_id.copy()
                    fields = self.env['product.template']._fields
                    #for fld in fields :
                    copyitem.write({'cn_configid': self.affected_product_id.cn_configid})
                    copyitem.write({'cnis_current': False})
                    copyitem.write({'active': False})
                    copyitem.write({'name': self.affected_product_id.name})
                    copyitem.write({'version': self.affected_product_id.version+1})                 
                    copyitem.write({'state': "Draft"})
                    self.write ({'new_affected_product_id':copyitem.id})  
                    self.affected_product_id.write({'state':'InChange'}) 
                    self.affected_product_id.write({'active':True})
                    self.affected_product_id.write({'cnis_current':True})     
                    
                else :
                    self.affected_product_id.write({'state':'Review'})
                    self.write({'new_affected_product_id':self.affected_product_id.id}) 
            else :
                if self.flow_class =='Bom' and self.affected_bom_id != False :
                    #if self.producaffected_product_idtion_id:
                    # This ECO was generated from a MO. Uses it MO as base for the revision.


                 if self.affected_bom_id.version !=1  or self.affected_bom_id.state == 'Released':
                    if not self.new_affected_bom_id:
                        self.new_affected_bom_id = self.affected_bom_id.sudo().copy(default={
                            'version': self.affected_bom_id.version + 1,
                            'active': False,
                            'cnis_current': False,
                        })
                        self.affected_bom_id.write ({'active':True}) 
                        self.affected_bom_id.write({'state':'InChange'}) 
                        self.affected_bom_id.write({'cnis_current':True})
                        self.write({'new_affected_bom_id':self.new_affected_bom_id.id})   
                    
                else :
                    self.affected_bom_id.write({'state':'Review'})
                    self.write({'new_affected_bom_id':self.affected_bom_id.id}) 
                    
                   
                    
            # ebert end             
             
        elif self.state =='Review':
            raise UserError('已是"审核中"状态')
        else:
            raise UserError('不可以推到"审核中"状态')
   
    def action_set_Review_after(self):
        if self.flow_class =='Product':                
            self.new_affected_product_id.write({'state':'Review'})  
        elif self.flow_class =='Bom' and self.affected_bom_id != False :                
                self.affected_bom_id.write({'state':'Review'}) 
        elif self.state =='Review':
            raise UserError('已是"变更后审核"状态')
        else:
            raise UserError('不可以推到"变更后审核"状态')  

    def action_set_Approved(self):
        if self.state =='Review':
            self.write({'state':'Approved'})

             #ebert 发布 Released
            if self.flow_class =='Product':
                
                if self.affected_product_id.version !=1  or self.affected_product_id.state == 'InChange':
                    self.affected_product_id.write({'state':'Superseded'}) 
                    self.affected_product_id.write({'active':False}) 
                    self.affected_product_id.write({'cnis_current':False}) 
                    self.new_affected_product_id.write({'active':True}) 
                    self.new_affected_product_id.write({'state':'Released'}) 
                    self.new_affected_product_id.write({'cnis_current':True}) 
                else :
                    self.affected_product_id.write({'state':'Released'})
            else :
                if self.flow_class =='Bom' and self.affected_bom_id != False  :
                    #if self.producaffected_product_idtion_id:
                    # This ECO was generated from a MO. Uses it MO as base for the revision.

                    if self.affected_bom_id.version !=1  or self.affected_bom_id.state == 'InChange':
                        self.affected_bom_id.write({'state':'Superseded'}) 
                        self.affected_bom_id.write({'active':False}) 
                        self.affected_bom_id.write({'cnis_current':False})
                        self.new_affected_bom_id.write({'active':True}) 
                        self.new_affected_bom_id.write({'state':'Released'}) 
                        self.new_affected_bom_id.write({'cnis_current':True}) 
                    else :
                        self.new_affected_bom_id.write({'state':'Released'})

                     
            # ebert end 



              
        elif self.state =='Approved':
            raise UserError('已是"核准"状态')
        elif self.state =='Cancel':
            raise UserError('已取消,不能被核准')
        else:
            raise UserError('不可以推到"核准"状态')
    def action_set_Cancel(self):
        if self.state =='New':
            self.write({'state':'Cancel'})
        elif self.state =='Review':
            self.write({'state':'Cancel'})             
        elif self.state =='Cancel':
            raise UserError('已是"取消"状态')
        else:
            raise UserError('已核准,不能被取消')


#抄写A 栏位的内容 到C栏位中
    @api.depends('product_name')
    def _compute_c(self):
          for record in self:
                record.title =f"{record.product_name}"

# PCO状态改变,Product_templete状态也跟着改变
    # @api.onchange('state')
    # def _update_pt_state(self):  
    #     if self.state == 'Review':  # 状态1是模块A的一个状态  
    #         self.affected_product_id.state= 'Review'# 对应地更新模块B的状态
    #     elif self.state == 'Approved':  
    #         self.affected_product_id.state= 'Released'
    #     else:
    #         pass

    # ebert
    def open_new_bom(self):
        self.ensure_one()
        return {
            'name': _('Pco BoM'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mrp.bom',
            'target': 'current',
            'res_id': self.new_affected_bom_id.id,
            'context': {
                'default_product_tmpl_id': self.new_affected_product_id.id,
                'default_product_id': self.new_affected_product_id.product_variant_id.id,
                'create': self.state != 'done',
                'edit': self.state != 'done',
                'delete': self.state != 'done',
            },
        }
    
    def open_new_product(self):
         if self.affected_product_id.version == 1 and (self.affected_product_id.state != 'Released'  and self.affected_product_id.state != 'InChange' and self.state != 'Approved' )   :
            raise UserError('新版发布,打开为空！')
         else :
            self.ensure_one()
            return {
                'name': _('Pco Product'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'product.template',
                'target': 'current',
                'res_id': self.new_affected_product_id.id,
                'context': {
                    'default_product_tmpl_id': self.new_affected_product_id.id,
                    'default_product_id': self.new_affected_product_id.product_variant_id.id,
                    'create': self.state != 'done',
                    'edit': self.state != 'done',
                    'delete': self.state != 'done',
                },
        }
    
    #ebert show version
    def _comput_show_version(self) :
         for record in self:
            if self.affected_product_id :
                record.affected_product_version = record.affected_product_id.version
            
            if self.new_affected_product_id :
                record.new_affected_product_version = record.new_affected_product_id.version
           

    def _comput_show_version_p(self) :
        for record in self:
            if self.affected_bom_id :
                raise UserError('test,')
                record.affected_bom_version = record.affected_bom_id.version
            # if self.new_affected_bom_id :
            #     record.new_affected_bom_version = record.new_affected_bom_id.version

