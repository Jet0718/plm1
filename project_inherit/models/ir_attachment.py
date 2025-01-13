from odoo import api,fields, models,_
import base64
from odoo.exceptions import UserError
from odoo import http
from odoo.http import request

# from odoo import http
# import json
# from odoo.http import request
# import base64
# import openpyxl
# from io import BytesIO

class InhtProjectModel(models.Model):
    _name = "ir.attachment"
    _description="Ir Attachment"
    _inherit = ['revision.plm.mixin', 'ir.attachment']    
    
    #ebert
    active = fields.Boolean(string ="启用",default=True,readonly=True)
    owner=fields.Many2one('res.users', default=lambda self: self.env.user.id, string="責任人")
    contactor =fields.Many2one('res.partner', string="聯絡人")
    cnis_current = fields.Boolean('isCurrent', default=True,readonly=True)
    cn_configid = fields.Char(string='configid',default="0",readonly=True)
    cn_file2prj = fields.Many2many('project.project',string='项目')
    cn_file2prd = fields.Many2many('product.template',string='产品')
    cn_cadfile_ships = fields.One2many('ir.attachment.ships','iship_id','子阶图纸')

    url = fields.Char(string="URL")
    iframe_html = fields.Html(string='Iframe Preview', compute='_compute_iframe_html', sanitize=False)    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('engineering_code'):
                vals['engineering_code'] = self.env['ir.sequence'].next_by_code('irattachmenseq')
                # vals['cn_configid'] = vals.get('id')                
        res = super().create(vals_list)
        if res.cn_configid =="0" :
            res.write({'cn_configid': res.id,'public':True})

        # 从 name 字段中提取文件后缀名
        if res.name:
            file_name = res.name
            # file_extension = file_name.split('.')[-1].lower() if '.' in file_name else ''
            if file_name.lower().endswith('.pdf'):
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                thisid=res.id
                pdf_url =  f"{base_url}/web/static/lib/pdfjs/web/viewer.html?file={base_url}/web/content?model=ir.attachment%26field=datas%26id={thisid}#page=1"            
                res.write({"url":pdf_url}) 
                



        return res
    
    #ebert按钮跳转页面    
    def action_openfileversions(self): 
         return {
            'name': '历程记录',
            'res_model': 'ir.attachment', 
            'view_mode': 'tree,form',
            #'view_id': self.env.ref('product.template.product_template_tree_view').id,   
            'domain': [('active', '=', False),('cn_configid', '=', self.cn_configid)],  
            'context': {'disable_preview': 1, 'form_view_ref': 'project_inherit.view_attachfileprj_form_inherit'},
            'type': 'ir.actions.act_window',
        }


   

    @api.depends('url')
    def _compute_iframe_html(self):
        for record in self:
            if record.url:
                record.iframe_html = f'<iframe src="{record.url}" width="100%" height="500px" frameborder="0" allowfullscreen></iframe>'
            else:
                record.iframe_html = False

    def action_open_pdf(self):
         return {
                'type': 'ir.actions.act_window',
                'name': 'PDF View',
                'res_model': 'ir.attachment',  # 可以是任意模型
                'view_mode': 'form',
                'view_id': self.env.ref('project_inherit.custom_iframe_view').id,  # 自定义视图
                'target': 'new',  # 打开浮层对话框
                'context': {
                    'default_url': self.url,  # 传递动态生成的 URL
                },
            }
        # 假设所有PDF文件都是内容类型为'application/pdf'
        # pdf_attachment = self.env['ir.attachment'].search([('id', '=', self.id)], limit=1)
        # if pdf_attachment.datas and pdf_attachment.name.lower().endswith('.pdf'):
        #     base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        #     pdf_url =  f"{base_url}/web/static/lib/pdfjs/web/viewer.html?file={base_url}/web/content?model=ir.attachment%26field=datas%26id={self.id}#page=1"            
        #     self.write({"url":pdf_url})            
        #     return {
        #         'type': 'ir.actions.act_window',
        #         'name': 'PDF View',
        #         'res_model': 'ir.attachment',  # 可以是任意模型
        #         'view_mode': 'form',
        #         'view_id': self.env.ref('project_inherit.custom_iframe_view').id,  # 自定义视图
        #         'target': 'new',  # 打开浮层对话框
        #         'context': {
        #             'default_url': pdf_url,  # 传递动态生成的 URL
        #         },
        #     }
        # else:
        #     self.write({"url":""})
            
    
    @api.onchange('datas')
    def _onchange_datas(self):
        #  当 datas 字段发生变化时，自动提取文件后缀名并存储到 file_extension 字段
        for attachment in self:
            if attachment._origin and attachment.name :
                # 从 name 字段中提取文件后缀名
                file_name = attachment.name
                # file_extension = file_name.split('.')[-1].lower() if '.' in file_name else ''
                if file_name.lower().endswith('.pdf'):
                    base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                    thisid=attachment._origin.id
                    pdf_url =  f"{base_url}/web/static/lib/pdfjs/web/viewer.html?file={base_url}/web/content?model=ir.attachment%26field=datas%26id={thisid}#page=1"            
                    attachment.write({"url":pdf_url}) 
                else:                    
                    self.write({"url":""})
            # elif not attachment._origin  and attachment.name :
                


