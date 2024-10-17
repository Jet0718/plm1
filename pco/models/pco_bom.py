from odoo import api,fields, models,_
from datetime import timedelta
from odoo.exceptions import UserError

class PCOBomModel(models.Model):
    _name = "pco.bom"
    _description = "PCO_BOM main model for PCO."
    _inherit = ['mail.thread','mail.activity.mixin']
        
    pco_id_bom =fields.Many2one("pco")
    affected_bom_id =fields.Many2one('mrp.bom',string='审批物料清单') 
    active =fields.Boolean("啟用",default=True)   
    new_affected_bom_id =fields.Many2one('mrp.bom',string='新版物料清单')
    #添加显示版本
    affected_bom_version = fields.Integer('物料清单旧版本',  related='affected_bom_id.version', readonly=True)
    new_affected_bom_version = fields.Integer('物料清单新版本',  related='new_affected_bom_id.version', readonly=True)

    