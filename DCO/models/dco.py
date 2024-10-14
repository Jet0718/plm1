from odoo import api,fields, models,_
from datetime import timedelta
from odoo.exceptions import UserError

class DCOModel(models.Model):
    _name = "dco"
    _description = "DCO main model for OpenPLM."
    _inherit = ['mail.thread','mail.activity.mixin']
        
    item_number =fields.Char("編號" , default=lambda self: _('New'), copy=False , readonly=True )
    title=fields.Char("主旨" ,required=True,readonly=False) 
    description=fields.Char("說明")
    flow_class =fields.Selection(
        string="審批類別",
        selection=[('Technical','技术文件'),('System','体系文件')],
        required=True
    )
    owner_id =fields.Many2one('res.users',string='責任人',default=lambda self: self.env.user)
    contactor_id =fields.Many2one('res.users',string='核決者',required=True)  
    tag_ids = fields.Many2many('dco.tag', string='Tags')
    state =fields.Selection(
        string="状态",
        selection=[('New','草稿'),('Review','审核中'),('Approved','核准'),('Cancel','取消')],
        default="New",readonly=True,tracking=1
    )
    # #需串联碧涛哥写的工程文件
    affected_item_id =fields.Many2one('dms.file',string='審批文件',options={'no_create': True}, ondelete='cascade', auto_join=True, copy=False)
    # #没法串联碧涛哥写的工程文件,暂代写法  
    #affected_item_id =fields.Char("審批文件")
    active =fields.Boolean("啟用",default=True)    

    # #上传单个档案写法
    # binary_field = fields.Binary("档案")
    # binary_file_name =fields.Char("档案名称")
    # #上传多个档案写法
    binary_fields =fields.Many2many("dms.file",string="Multi Files Upload")

    #ebert 
    
    #添加显示版本 ,related='new_affected_item_id.version' ,related='affected_item_id.version'
    affected_item_version = fields.Integer('旧版本', readonly=True,default=False,related='affected_item_id.version')
    
    new_affected_item_id =fields.Many2one('dms.file',string='新版審批文件', readonly=True)
    new_affected_item_version = fields.Integer('新版本',related='new_affected_item_id.version',   readonly=True)
    #ebert end 

    # Seqence 自动领号写法 compute='_comput_show_version',  ,related='new_affected_item_id.version'
    @api.model_create_multi
    def create(self, vals_list):
         """ Create a sequence for the requirement model """
         for vals in vals_list:
               if vals.get('item_number', _('New')) == _('New'):
                      vals['item_number'] = self.env['ir.sequence'].next_by_code('dco')
                      return super().create(vals_list)     
    
    #定义按钮
    def action_set_Review(self):
        if self.state =='New':
            self.write ({'state':'Review'})  
            #ebert             
            if self.affected_item_id.version !=1  or self.affected_item_id.state == 'Released':
                self.affected_item_id.write({'active':False})
                copyitem=self.affected_item_id.copy()
                fields = self.env['product.template']._fields
                #for fld in fields :
                copyitem.write({'cn_configid': self.affected_item_id.cn_configid})
                copyitem.write({'cnis_current': False})
                copyitem.write({'active': False})
                copyitem.write({'name': self.affected_item_id.name})
                copyitem.write({'version': self.affected_item_id.version+1})                 
                copyitem.write({'state': "Draft"})
                self.write ({'new_affected_item_id':copyitem.id})  
                self.affected_item_id.write({'state':'InChange'}) 
                self.affected_item_id.write({'active':True})
                #self.affected_item_id.write({'cnis_current':True})     
                
            else :
                self.affected_item_id.write({'state':'Review'})
                self.write({'new_affected_item_id':self.affected_item_id.id}) 
            #ebert end
        elif self.state =='Review':
            raise UserError('已是"审核中"状态')
        else:
            raise UserError('不可以推到"审核中"状态')
        
    def action_set_Review_after(self):                       
        self.new_affected_item_id.write({'state':'Review'})  
        
          
    def action_set_Approved(self):
        if self.state =='Review':
            self.write({'state':'Approved'})

            if self.affected_item_id.version !=1  or self.affected_item_id.state == 'InChange':
                self.affected_item_id.write({'state':'Superseded'}) 
                self.affected_item_id.write({'active':False})  
                self.affected_item_id.write({'cnis_current':False}) 
                self.new_affected_item_id.write({'active':True})                 
                self.new_affected_item_id.write({'cnis_current':True}) 
                self.new_affected_item_id.write({'state':'Released'}) 
                
            else :
                self.affected_item_id.write({'state':'Released'})
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

    #ebert show version
    def _comput_show_version(self) :
         for record in self:
            if self.affected_item_id :
                record.affected_item_version = record.affected_item_id.version
            if self.new_affected_item_id :
                record.new_affected_item_version = record.new_affected_item_id.version
            # if self.new_affected_product_id :
            #     record.new_affected_product_id_version = record.new_affected_product_id.version
            # if self.new_affected_bom_id :
            #     record.new_affected_bom_id_version = record.new_affected_bom_id.version



