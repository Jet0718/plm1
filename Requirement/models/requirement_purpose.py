from odoo import api,fields, models
from datetime import timedelta

class requirement_purpose(models.Model):
    _name = "requirement.purpose"
    name =fields.Char("用途名称",required=True)