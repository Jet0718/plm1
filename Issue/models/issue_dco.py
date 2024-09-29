from odoo import fields, models,api,_

class PCOModel(models.Model):
    _inherit = "dco"
    # 2024.9.25 Herbert新增内容:增加关联issue 及 issue数量
    issue_ids = fields.One2many('issue','dco_id')
    issue_count =fields.Integer("数量" ,compute='_compute_issue_count')

#计算关联Issue的数量
    @api.depends("issue_ids")
    def _compute_issue_count(self):
        for record in self:
            record.issue_count = len(record.issue_ids)


