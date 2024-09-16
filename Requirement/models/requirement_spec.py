from odoo import api,fields, models
from datetime import timedelta

class requirement_purpose(models.Model):
    _name = "requirement.spec"
    name =fields.Char("名称",required=True)
    description = fields.Char("说明")
    requirement_id =fields.Many2one('requirement',sting ='需求评估')