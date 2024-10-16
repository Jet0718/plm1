from odoo import fields, models,api,_

class ProductTemplate(models.Model):
    _inherit = "product.template"
    # 2024.9.25 Herbert新增内容:增加关联issue 及 issue数量
    issue_ids = fields.One2many('issue','issue_product_id')
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
            'domain': [('issue_product_id', '=', self.id) ],
            'context': {'default_issue_product_id': self.id},
        }