from odoo import api,fields, models
from datetime import timedelta

class requirement_purpose(models.Model):
    _name = "requirement.purpose"
    _description = "purpose lib model for require management."
    name =fields.Char("用途名称",required=True)