from odoo import fields, models,api,_
from odoo.exceptions import UserError

class PCOModel(models.Model):
    _inherit = "pco"
    # 2024.9.25 Herbert新增内容:增加关联issue 及 issue数量
    issue_ids = fields.One2many('issue','pco_id')
    issue_count =fields.Integer("数量" ,compute='_compute_issue_count',default=0)

#计算关联Issue的数量
    @api.depends("issue_ids")
    def _compute_issue_count(self):
        for record in self:  
            try: 
                record.issue_count = len(record.issue_ids)                
            except Exception as e:                
                record.issue_count =self.env['issue'].search_count([('pco_id', '=', record.id)])

    def issue_model_action(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'issue',
            'view_mode': 'tree,form',
            'res_model': 'issue',
            'domain': [('pco_id', '=', self.id) ],
            'context': {'default_pco_id': self.id},
        }
