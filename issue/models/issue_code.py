from odoo import api,fields, models,_
from datetime import timedelta

class requirement_purpose(models.Model):
    _name = "issue.code"
    _description = "issue code model for Issue. "
    _inherit = ['mail.thread','mail.activity.mixin']
    
    item_number =fields.Char("问题代码" , default=lambda self: _('New'), copy=False , readonly=True )
    name =fields.Char("问题编码主旨",required=True)
    description = fields.Char("问题编码说明",compute='_compute_c',required=True,readonly=False)
    class1 =fields.Selection(
        string="问题编码分类一",
        selection=[('人','人'),('机','机'),('料','料'),
                   ('法','法'),('环','环'),('测','测'),('设计开发','设计开发')],
        required=True
    )
    class2a =fields.Selection(
        string="问题编码分类二",
        selection=[('组装错误','组装错误'),('治具选择错误','治具选择错误'),('未按SOP操作','未按SOP操作')]
    )   
    class2b =fields.Selection(
        string="问题编码分类二",
        selection=[('设备维护保养问题','设备维护保养问题'),('工具损坏','工具损坏')]
    )    
    class2c =fields.Selection(
        string="问题编码分类二",
        selection=[('冷水机异常','冷水机异常'),('控制屏异常','控制屏异常'),('配电板','配电板'),('保护镜异常','保护镜异常')]
    )  
    class2d =fields.Selection(
        string="问题编码分类二",
        selection=[('缺少流程类文件','缺少流程类文件'),('缺少记录模版','缺少记录模版')]
    )  
    class2e =fields.Selection(
        string="问题编码分类二",
        selection=[('状态标识问题','状态标识问题'),('温湿度超标','温湿度超标')]
    )  
    class2f =fields.Selection(
        string="问题编码分类二",
        selection=[('测试环境问题','测试环境问题'),('测试SOP错误或不适用','测试SOP错误或不适用')]
    )  
    class2g =fields.Selection(
        string="问题编码分类二",
        selection=[('硬件设计开发缺陷','硬件设计开发缺陷')]
    )     
    class3c1 =fields.Selection(
        string="问题编码分类三",
        selection=[('漏氟','漏氟'),('泵','泵'),('水流开关','水流开关')]
    )  
    class3c3 =fields.Selection(
        string="问题编码分类三",
        selection=[('时间继电器','时间继电器'),('控制继电器','控制继电器')]
    )  
    class3c4 =fields.Selection(
        string="问题编码分类三",
        selection=[('朝光纤面损坏','朝光纤面损坏')]
    )      
# Seqence 自动领号写法
    @api.model_create_multi
    def create(self, vals_list):
         """ Create a sequence for the requirement model """
         for vals in vals_list:
               if vals.get('item_number', _('New')) == _('New'):
                      vals['item_number'] = self.env['ir.sequence'].next_by_code('issue.code')
                      return super().create(vals_list)     
#抄写A 和 B 栏位的内容 到C栏位中
    @api.depends('class1', 'name')
    def _compute_c(self):
          for record in self:
                record.description =f"{record.name}-{record.class1}"