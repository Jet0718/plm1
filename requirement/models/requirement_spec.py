from odoo import api,fields, models
from datetime import timedelta

class requirement_purpose(models.Model):
    _name = "requirement.spec"
    _description = "spec lib model for require management. "
    _inherit = ['mail.thread','mail.activity.mixin']
    
    name =fields.Char("名称",required=True)
    description = fields.Char("说明")
    requirement_id =fields.Many2one('requirement',string ='需求评估')