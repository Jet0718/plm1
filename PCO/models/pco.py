from odoo import api,fields, models,_
from datetime import timedelta
from odoo.exceptions import UserError

class PCOModel(models.Model):
    _name = "pco"
    _description = "PCO main model for OpenPLM."
    _inherit = ['mail.thread','mail.activity.mixin']
        
    item_number =fields.Char("編號" , default=lambda self: _('New'), copy=False , readonly=True )
    title=fields.Char("主旨" ,compute='_compute_c',required=True,readonly=False) 
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

    # #上传单个档案写法
    # binary_field = fields.Binary("档案")
    # binary_file_name =fields.Char("档案名称")
    # #上传多个档案写法
    binary_fields =fields.Many2many("ir.attachment",string="Multi Files Upload")

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
        elif self.state =='Review':
            raise UserError('已是"审核中"状态')
        else:
            raise UserError('不可以推到"审核中"状态')
    def action_set_Approved(self):
        if self.state =='Review':
            self.write({'state':'Approved'})
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


