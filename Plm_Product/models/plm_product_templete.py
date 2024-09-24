from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    state =fields.Selection(
        string="状态",
        selection=[('New','草稿'),('Review','审核中'),('Released','已发行'),('InChange','变更中'),('Superseded','作废')],
        default="New",readonly=True,tracking=1
    )