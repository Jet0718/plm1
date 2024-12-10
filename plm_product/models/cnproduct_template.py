from odoo import api,fields, models,_

from odoo.exceptions import UserError
from collections import Counter

class InhtProducttmpModel(models.Model):
    _inherit = "product.template"

    item_number = fields.Char(string="編號",default=lambda self:_("no"),copy=False,readonly=True)
    xspec       = fields.One2many('product.spec', 'prd_id', '規格特性')
    state = fields.Selection([
            ('draft', 'Draft'),
            ('confirmed', 'Review'),
            ('released', 'Released'),            
            ('undermodify', 'UnderModify'),
            ('obsoleted', 'Obsoleted')],string = "狀態",
            copy=False, default='draft', readonly=True, required=True, index=True)     

    #ebert         
    #cn_is_current = fields.Boolean('is Current', default=True)
    cnis_current = fields.Boolean('isCurrent', default=True,readonly=True)
    cn_configid = fields.Char(string='configid',default="0",readonly=True)
    
    pdt2pdt_id = fields.Many2one(
        'product.template', 'product_template',
        ondelete='cascade', required=False)
    cn_pdt2version_ship = fields.One2many('product.template', 'pdt2pdt_id', '历程记录')
    version=fields.Integer("version",default=1,copy=False,readonly=True)

    engineering_code = fields.Char(string="Engineering Code",readonly=True)
    # default_code = fields.Char(string="Internal Reference",readonly=True)
    # is_engcode_editable = fields.Boolean('Engineering Editable', default=True, compute=lambda self: self._compute_eng_code_editable1())


    @api.model_create_multi
    def create(self,vals_list):          
        for vals in vals_list:
            encode=vals.engineering_code           
            if not encode:
                vals['engineering_code'] =self.env['ir.sequence'].next_by_code('plm.eng.code')  
                 
        
        res  = super().create(vals_list) 
        if res :
            for record in res :
                # raise UserError(str(record.id)+' 000 '+record.cn_configid)
                if  record.cn_configid =="0"  :
                    record.write({'cn_configid':record.id})

              
        
        producnt = self.env['product.product'].search([('engineering_code', "=", res.engineering_code),('engineering_revision','=',res.engineering_revision)])
        if len(producnt) == 1 :
            try :
                count = Counter(producnt.default_code)
            except OSError as ex:
                count=0
            if count !=2 :
                producnt.write({'default_code': res.engineering_code +'_01_'+str(res.engineering_revision)})
        return res


    @api.onchange("categ_id")
    def onchange_categ_id(self):
        return self
         
    #ebert按钮跳转页面    
    def action_open_versions(self): 
         return {
            'name': '历程记录',
            'res_model': 'product.template', 
            'view_mode': 'tree,form',
            #'view_id': self.env.ref('product.template.product_template_tree_view').id,   
            'domain': [('active', '=', False),('cn_configid', '=', self.cn_configid)],  
            'context': {'disable_preview': 1, 'form_view_ref': 'plm_product.product_template_only_form_inherit_itemnumber'},
            'type': 'ir.actions.act_window',
        }

    def _create_variant_ids(self): 
         # 呼叫原有方法
        result = super(InhtProducttmpModel, self)._create_variant_ids()
        prent_engineering_code=self.engineering_code
        prent_engineering_revision=self.engineering_revision
        # pass
        # 在這裡添加自訂邏輯，
        producnts=self.env['product.product'].search([('engineering_code', "=", prent_engineering_code),('engineering_revision','=',prent_engineering_revision)])
        i=0
        for record in producnts:
            i=i+1
            
            setflog = False
            if not record.default_code :
                setflog = True
            else :
                
               
                try :
                    count = Counter(record.default_code)
                except OSError as ex:
                    count=0
                if count ==2 :
                    setflog = True
            
            if setflog :
                engineering_revision =record.engineering_revision
                vstr = str(i).zfill(2)
                record.write({'default_code': prent_engineering_code+'_' +vstr+'_'+str(engineering_revision)})
        

    # def _compute_eng_code_editable1(self):
    #     for productBrws in self:
    #         productBrws.is_engcode_editable = True


class productSpec(models.Model):
    _name="product.spec"
    _description="Specification for Part"

    prd_id=fields.Many2one('product.template',"product",required=True)

    name = fields.Char(string="規格名稱")
    description= fields.Char(string="內容")

# class productSpec(models.Model):    
#     _inherit = 'revision.plm.mixin'
#     # _inherit = ['mail.thread','mail.activity.mixin']
#     _description = 'Revision Mixin'
#     #
#     engineering_revision = fields.Integer(string="Engineering Revision index", default=1)
#     engineering_revision_letter = fields.Char(string="Engineering Revision letter", default="A")
#     #
#     engineering_branch_revision = fields.Integer(string="Engineering Branch index", default=1)
#     engineering_branch_revision_letter = fields.Char(string="Engineering Sub Revision letter", default="A")




