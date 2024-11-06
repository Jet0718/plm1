from odoo import api,fields, models,_

from collections import Counter
from odoo.exceptions import UserError

class InhtProductModel(models.Model):
    _inherit = "product.product"

    # engineering_code = fields.Char(string="Engineering Code",readonly=True)
    # default_code = fields.Char(string="Internal Reference",readonly=True)
         
    #ebert按钮跳转页面    
    def action_open_versions(self): 
         return {
            'name': '历程记录',
            'res_model': 'product.product', 
            'view_mode': 'tree,form',
            #'view_id': self.env.ref('product.template.product_template_tree_view').id,   
            'domain': [('active', '=', False),('cn_configid', '=', self.cn_configid)],  
            #'context': {'search_default_group': 'my_group'},
            'type': 'ir.actions.act_window',
        }
    
    @api.model_create_multi
    def create(self,vals_list):  
        res =super().create(vals_list)   
        
        
        new_vals_list = []
        setflog = False
        for vals in res:           
            encode=vals.engineering_code
            engineering_revision =vals.engineering_revision
            code =vals.default_code
              
            if not code and encode :
                setflog = True            
            else :
                try :
                    
                    count = Counter(code)
                except OSError as ex:
                    count=0
                if count ==2 :
                    setflog = False
            if setflog:
                strv=encode + '_01_' + str(engineering_revision)
                vals["default_code"]= strv
                vals.write({'default_code': strv})
                
            
            # # raise UserError(strv)
            # new_vals_list.append(vals)
            # if setflog :
            #     return super().create(new_vals_list)
            else :  
                
                if res :
                    encode=res.engineering_code 
                    engineering_revision =res.engineering_revision
                    code =res.default_code 
                    try :
                        count = Counter(code)
                    except OSError as ex:
                        count=0
                        return res
                    if not count or  count !=2 :
                        strv=encode + '_01_' + str(engineering_revision)
                        # raise UserError(strv+' 000')
                        res.write({'default_code': strv})
        return res
       
                
        
        
