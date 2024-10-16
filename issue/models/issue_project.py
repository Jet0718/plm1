from odoo import fields, models,api,_

class Project(models.Model):
    _inherit = "project.project"
    # 2024.9.25 Herbert新增内容:增加关联issue 及 issue数量
    issue_ids = fields.One2many('issue','project_id')
    issue_count =fields.Integer("数量" ,compute='_compute_issue_count')
#计算关联Issue的数量
    @api.depends("issue_ids")
    def _compute_issue_count(self):
        for record in self:
            record.issue_count = len(record.issue_ids)

    def issue_model_action(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'issue',
            'view_mode': 'tree,form',
            'res_model': 'issue',
            'domain': [('project_id', '=', self.id) ],
            'context': {'default_project_id': self.id},
        }