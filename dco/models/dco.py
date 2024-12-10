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
    affected_item_id =fields.Many2one('ir.attachment',string='審批文件',options={'no_create': True}, ondelete='cascade', auto_join=True, copy=False)
    # #没法串联碧涛哥写的工程文件,暂代写法  
    #affected_item_id =fields.Char("審批文件")
    active =fields.Boolean("啟用",default=True)    

    # #上传单个档案写法
    # binary_field = fields.Binary("档案")
    # binary_file_name =fields.Char("档案名称")
    # #上传多个档案写法
    binary_fields =fields.Many2many("ir.attachment",string="Multi Files Upload" ,domain="['&',('engineering_code', '!=', ''),('is_plm', '=', True),('engineering_state', 'not in', ['obsoleted','undermodify']) ,('res_model','=',False),('active','=',True)]")

    #ebert 
    
    #添加显示版本 ,related='new_affected_item_id.version' ,related='affected_item_id.version'
    affected_item_version = fields.Integer('旧版本', readonly=True,default=False,related='affected_item_id.engineering_revision')
    
    new_affected_item_id =fields.Many2one('ir.attachment',string='新版審批文件', readonly=True)
    new_affected_item_version = fields.Integer('新版本',related='new_affected_item_id.engineering_revision',   readonly=True)
    #ebert end 

    dco_file_ids =fields.One2many('dco.file','dco_id',string=' ')

    btnflog=fields.Integer(default=1)

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
            for record in self.dco_file_ids:            
                if record.affected_item_id.engineering_revision !=0  or record.affected_item_id.engineering_state == 'released':
                    # record.affected_item_id.write({'active':False})
                    # copyitem=record.affected_item_id.copy()
                    # fields = record.env['product.template']._fields
                    # #for fld in fields :
                    # copyitem.write({'cn_configid': record.affected_item_id.cn_configid})
                    # copyitem.write({'cnis_current': False})
                    # copyitem.write({'active': False})
                    # copyitem.write({'name': record.affected_item_id.name})
                    # copyitem.write({'version': record.affected_item_id.engineering_revision+1})                 
                    # copyitem.write({'engineering_state': "draft"})
                    # 执行换版
                    record.affected_item_id.newVersion()
                    ecode = record.affected_item_id.engineering_code
                    eversion = record.affected_item_id.engineering_revision+1
                    
                    # raise UserError( record.affected_item_id.engineering_revision)
                    newrecord = self.env['ir.attachment'].search([('engineering_code', '=' ,ecode ),('engineering_revision', '=' ,eversion)])
                    # raise UserError( newrecord.engineering_revision)
                    newrecord.write({'cn_configid': record.affected_item_id.cn_configid,'cnis_current': True, 'active': False})
                    record.affected_item_id.write({'cnis_current': False })
                    record.write({'new_affected_item_id': newrecord.id})
                    self.write({'btnflog': False})
                    
                    # record.write ({'new_affected_item_id':newrecord.id})  
                    # record.affected_item_id.write({'engineering_state':'undermodify'}) 
                    # record.affected_item_id.write({'active':True})
                    #self.affected_item_id.write({'cnis_current':True})     
                    


                else :
                    record.affected_item_id.action_confirm()
                    # record.affected_item_id.write({'engineering_state':'confirmed'})
                    record.write({'new_affected_item_id':record.affected_item_id.id}) 
            #ebert end
        elif self.state =='Review':
            raise UserError('已是"审核中"状态')
        else:
            raise UserError('不可以推到"审核中"状态')
        
    def action_set_Review_after(self): 
        for record in self.dco_file_ids:                    
            # record.new_affected_item_id.write({'engineering_state':'confirmed'})  
            if record.new_affected_item_id.engineering_state == 'draft' :
                record.new_affected_item_id.action_confirm()
        self.write({'btnflog': True})
          
    def action_set_Approved(self):
        if self.state =='Review':
            self.write({'state':'Approved'})
            
            for record in self.dco_file_ids:
                if record.affected_item_id.engineering_revision !=0  or record.affected_item_id.engineering_state == 'undermodify':
                    record.affected_item_id.write({'engineering_state':'obsoleted'}) 
                    record.affected_item_id.write({'active':False})  
                    record.affected_item_id.write({'cnis_current':False}) 
                    record.new_affected_item_id.write({'active':True})                 
                    record.new_affected_item_id.write({'cnis_current':True}) 
                    # record.new_affected_item_id.write({'engineering_state':'released'}) 

                    # record.affected_item_id.action_obsolete()
                    record.new_affected_item_id.action_release()

                    
                    
                else :
                    record.affected_item_id.action_release()
                    # record.affected_item_id.write({'engineering_state':'released'})
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

    # @api.onchange('dco_file_ids','state')
    # def _onchange_dco_file_ids(self):
    #     for record in self.dco_file_ids:
    #         # (not affected_item_id and not new_affected_item_id) or state !='Review' or affected_item_id.version ==1
    #         if  record.affected_item_id.engineering_revision !=0 or record.new_affected_item_id.engineering_revision !=0:
    #             self.write({'btnflog':0})
    def write(self, vals):        
        # raise UserError(typestr)
        # self.write({'btnflog':1})        
        # for record in self:
        #     for nd in record.pco_product_id:
        #         if res.state =='Review' and nd.new_affected_product_id.version !=1:
        #             self.write({'btnflog':0})
        #     for nd in record.pco_bom_ids:
        #         if res.state =='Review' and nd.new_affected_bom_id.version !=1:
        #             self.write({'btnflog':0})
        
        for record in self.dco_file_ids: 
            if record.new_affected_item_id and  record.new_affected_item_id.engineering_state == 'confirmed':
               res =  super(DCOModel, self).write(vals)                
               return res
            
        btnflog= True
        for record in self:
            for nd in record.dco_file_ids:
                if record.state =='Review' and (nd.affected_item_id.engineering_revision !=0  or nd.new_affected_item_id.engineering_revision !=0):
                    btnflog= False                    
        vals['btnflog'] =btnflog
        res =  super(DCOModel, self).write(vals)

        return res


