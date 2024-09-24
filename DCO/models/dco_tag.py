from odoo import api,fields, models
from datetime import timedelta

class requirement_purpose(models.Model):
    _name = "dco.tag"
    _description = "tag model for dco. "
    _inherit = ['mail.thread','mail.activity.mixin']
    
    name =fields.Char("标签名称",required=True)
    description = fields.Char("标签说明")