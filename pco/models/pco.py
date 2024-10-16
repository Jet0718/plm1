from odoo import api,fields, models,_
from datetime import timedelta
from odoo.exceptions import UserError

class PCOModel(models.Model):
    _name = "pco"
    _description = "PCO main model for OpenPLM."
    _inherit = ['mail.thread','mail.activity.mixin']
        
    item_number =fields.Char("編號" , default=lambda self: _('New'), copy=False , readonly=True )
    title=fields.Char("主旨" ,required=True,readonly=False,default=" ") 
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
    active =fields.Boolean("啟用",default=True) 
    pco_product_id =fields.Many2many('pco.product',string='送審物件')


    # #上传单个档案写法
    # binary_field = fields.Binary("档案")
    # binary_file_name =fields.Char("档案名称")
    # #上传多个档案写法
    binary_fields =fields.Many2many("dms.file",string="Multi Files Upload")
    btnflog=fields.Integer(string="顯示",default=1)
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
            names=""
            for record in self.pco_product_id: 
                # names=names+"," +record.affected_product_id.name
            # raise UserError(names)
            
            #ebert version item 换版 条件判断送审物件的版本是否是1， 是则送审发布，否则换版
                if self.flow_class =='Product':
                    
                    if record.affected_product_id.version !=1  or record.affected_product_id.state == 'Released':
                        copyitem=record.affected_product_id.copy()
                        fields = record.env['product.template']._fields
                        #for fld in fields :
                        copyitem.write({'cn_configid': record.affected_product_id.cn_configid})
                        copyitem.write({'cnis_current': False})
                        copyitem.write({'active': False})
                        copyitem.write({'name': record.affected_product_id.name})
                        copyitem.write({'version': record.affected_product_id.version+1})                 
                        copyitem.write({'state': "Draft"})
                        record.write ({'new_affected_product_id':copyitem.id})  
                        record.affected_product_id.write({'state':'InChange'}) 
                        record.affected_product_id.write({'active':True})
                        record.affected_product_id.write({'cnis_current':True})     
                        
                    else :
                        record.affected_product_id.write({'state':'Review'})
                        record.write({'new_affected_product_id':record.affected_product_id.id}) 
                else :
                    if self.flow_class =='Bom' and record.affected_bom_id != False :
                        #if self.producaffected_product_idtion_id:
                        # This ECO was generated from a MO. Uses it MO as base for the revision.


                        if record.affected_bom_id.version !=1  or record.affected_bom_id.state == 'Released':
                            if not record.new_affected_bom_id:
                                record.new_affected_bom_id = record.affected_bom_id.sudo().copy(default={
                                    'version': record.affected_bom_id.version + 1,
                                    'active': False,
                                    'cnis_current': False,
                                })
                                record.affected_bom_id.write ({'active':True}) 
                                record.affected_bom_id.write({'state':'InChange'}) 
                                record.affected_bom_id.write({'cnis_current':True})
                                record.write({'new_affected_bom_id':record.new_affected_bom_id.id})   
                            
                        else :
                            record.affected_bom_id.write({'state':'Review'})
                            record.write({'new_affected_bom_id':record.affected_bom_id.id}) 
                        
                   
                    
            # ebert end             
             
        elif self.state =='Review':
            raise UserError('已是"审核中"状态')
        else:
            raise UserError('不可以推到"审核中"状态')
   
    def action_set_Review_after(self):
        for record in self.pco_product_id: 
            if self.flow_class =='Product':                
                record.new_affected_product_id.write({'state':'Review'})  
            elif self.flow_class =='Bom' and record.affected_bom_id != False :                
                record.affected_bom_id.write({'state':'Review'}) 
        # elif self.state =='Review':
        #     raise UserError('已是"变更后审核"状态')
        # else:
        #     raise UserError('不可以推到"变更后审核"状态')  

    def action_set_Approved(self):
        if self.state =='Review':
            self.write({'state':'Approved'})

    #          #ebert 发布 Released
            for record in self.pco_product_id:
                if self.flow_class =='Product':
                    
                    if record.affected_product_id.version !=1  or record.affected_product_id.state == 'InChange':
                        record.affected_product_id.write({'state':'Superseded'}) 
                        record.affected_product_id.write({'active':False}) 
                        record.affected_product_id.write({'cnis_current':False}) 
                        record.new_affected_product_id.write({'active':True}) 
                        record.new_affected_product_id.write({'state':'Released'}) 
                        record.new_affected_product_id.write({'cnis_current':True}) 
                    else :
                        record.affected_product_id.write({'state':'Released'})
                else :
                    if self.flow_class =='Bom' and record.affected_bom_id != False  :
                        #if self.producaffected_product_idtion_id:
                        # This ECO was generated from a MO. Uses it MO as base for the revision.

                        if record.affected_bom_id.version !=1  or record.affected_bom_id.state == 'InChange':
                            record.affected_bom_id.write({'state':'Superseded'}) 
                            record.affected_bom_id.write({'active':False}) 
                            record.affected_bom_id.write({'cnis_current':False})
                            record.new_affected_bom_id.write({'active':True}) 
                            record.new_affected_bom_id.write({'state':'Released'}) 
                            record.new_affected_bom_id.write({'cnis_current':True}) 
                        else :
                            record.new_affected_bom_id.write({'state':'Released'})

                        
    #         # ebert end 
             
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
        

    
   
    @api.onchange('pco_product_id')
    def _compute_pco_product_id(self):
        self.write({'btnflog':1})
        for record in self:
            for nd in record.pco_product_id:
                if self.state =='Review' and (nd.new_affected_product_id.version !=1 or nd.new_affected_bom_id.version !=1):
                    self.write({'btnflog':0})