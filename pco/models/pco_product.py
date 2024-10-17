from odoo import api,fields, models,_
from datetime import timedelta
from odoo.exceptions import UserError

class PCOProductModel(models.Model):
    _name = "pco.product"
    _description = "PCO_product main model for PCO."
    # _inherit = ['mail.thread','mail.activity.mixin']
        
    pco_id_prd =fields.Many2one("pco")
    affected_product_id =fields.Many2one('product.template',string='審批产品')
    active =fields.Boolean("啟用",default=True)    
    #ebert 
    new_affected_product_id =fields.Many2one('product.template',string='新版審批产品')  
    #添加显示版本
    affected_product_version = fields.Integer('产品旧版本',  related='affected_product_id.version', readonly=True)
    new_affected_product_version = fields.Integer('产品新版本',  related='new_affected_product_id.version', readonly=True)
