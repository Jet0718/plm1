from odoo import api,fields, models,_
from datetime import timedelta
from odoo.exceptions import UserError

class PCOProductModel(models.Model):
    _name = "dco.file"
    _description = "dco file main model for DCO."
    _inherit = ['mail.thread','mail.activity.mixin']
        

    affected_item_id =fields.Many2one('dms.file',string='審批文件',options={'no_create': True}, ondelete='cascade', auto_join=True, copy=False)
     #添加显示版本 ,related='new_affected_item_id.version' ,related='affected_item_id.version'
    affected_item_version = fields.Integer('旧版本', readonly=True,default=False,related='affected_item_id.version')
    
    new_affected_item_id =fields.Many2one('dms.file',string='新版審批文件', readonly=True)
    new_affected_item_version = fields.Integer('新版本',related='new_affected_item_id.version',   readonly=True)