from odoo import models, fields, api,_
from datetime import datetime, timedelta

# models.TransientModel是零时数据，定期清理一帮7天左右

class InhtattchmentdlgModel(models.TransientModel):
    _name = "ir.attachmentdlg"
    _description="Ir Attachment dilog"

    url = fields.Char(string="URL")
    iframe_html = fields.Html(string='Iframe Preview', sanitize=False)


    @api.model_create_multi
    def create(self, vals_list):
         # 定义自定义的清理逻辑
        deletes=self.env['ir.attachmentdlg'].search([('id', '!=', False)])
        for d in  deletes:
            d.unlink()
        res = super().create(vals_list)
       
        return res

            

