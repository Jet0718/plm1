from odoo import api,fields, models,_
from datetime import datetime, timedelta
from odoo.exceptions import UserError
# 在你的odoo模块文件夹中创建一个controllers文件夹，并添加一个py文件，例如upload.py
from odoo import http
from odoo.http import request


class IssueModel(models.Model):
    _name = "issue"
    _description = "ISSUE main model for OpenPLM."    
    _inherit = ['mail.thread','mail.activity.mixin']

    item_number =fields.Char("问题編號" , default=lambda self: _('New'), copy=False , readonly=True )
    title=fields.Char("问题主旨")  
    issue_Source =fields.Selection(
        string="问题来源",
        selection=[('Customer','客户'),('Internal','内部'),('Supplier','供应商')],
        required=True
    )
    owner_id =fields.Many2one('res.users',string='问题回报人',default=lambda self: self.env.user)
    issue_product_id =fields.Many2one('product.template',string='问题产品')
    issue_bom_id =fields.Many2one('mrp.bom',string='问题物料清单') 
    external_number =fields.Char("外部单号")  
    priority = fields.Selection(
        [('0', 'Normal'),('1', 'Medium'),('2', 'High'),('3', 'Very High')],
        string='优先级', default='0')
    issue_stage= fields.Selection(
        [('Request Application', '需求申请'),('Design Fundamentals', '设计基础'),('Hierarchical structure', '层次结构'),
        ('Detailed design', '详细设计'),('Unique process', 'V项目独特工艺'),('Process standards', '工艺标准'),
        ('Build cycle', '构建周期'),('During testing', '测试中'),('In use', '使用中')],
        string='问题发生阶段')
    custoomer_id =fields.Many2one('res.company',string='受影响客户')
    description =fields.Text("问题描述") 
    environmental =fields.Text("环境说明") 
    reproduce = fields.Text("重现操作顺序")
    respond = fields.Selection(
        [('Y', 'Yes'),('N', 'No'),('NA', 'N/A')],
        string='回应')
    
    active =fields.Boolean("啟用",default=True) 
    quantity = fields.Integer("数量")
    issue_code_ids = fields.Many2many('issue.code', string='问题编码')
    state =fields.Selection(
        string="状态",
        selection=[('Submitted','提交'),('In Verification','验证中'),('Verified','已验证'),('Closed','关闭'),('Cancel','取消')],
        default="Submitted",readonly=True,tracking=1
    )
    #关联其他表单2024.9.25 Herbert增加
    project_id =fields.Many2one('project.project',string='关联专案')
    dco_id =fields.Many2many('dco',string='关联DCO')
    pco_id =fields.Many2many('pco',string='关联PCO')
    #增加栏位 2024.9.25 Herbert增加
    # solution =fields.Text("解决方案")
    vresults =fields.Selection(
        string="验证结果",
        selection=[('Acceptable','可接受'),('Observed','待观察')]
    ) 

    #增加欄位 2024.10.12 Herbert增加
    d3 =fields.Text("D3抑制措施")
    d4 =fields.Text("D4原因分析")
    d5 =fields.Text("D5纠正措施")
    d6 =fields.Text("D6执行问题改善")
    d7 =fields.Text("D7预防再发")
    team_id =fields.Many2many('res.users',string='团队人员')
    issue_image = fields.Image('圖片',max_width=128,max_height=128)

    
    # #上传单个档案写法
    # binary_field = fields.Binary("档案")
    # binary_file_name =fields.Char("档案名称")
    # #上传多个档案写法
    binary_fields =fields.Many2many("ir.attachment",string="Multi Files Upload",domain="['&',('engineering_code', '!=', ''),('is_plm', '=', True),('engineering_state', 'not in', ['obsoleted','undermodify']) ,('res_model','=',False),('active','=',True)]")

    # Seqence 自动领号写法
    @api.model_create_multi
    def create(self, vals_list):
         """ Create a sequence for the requirement model """
        
         for vals in vals_list:
               if vals.get('item_number', _('New')) == _('New'):
                      vals['item_number'] = self.env['ir.sequence'].next_by_code('issue')
        
         return super().create(vals_list)     
    
    #定义按钮
    def action_set_In_Verification(self):
        if self.state =='Submitted':
            self.write ({'state':'In Verification'})        
        elif self.state =='In Verification':
            raise UserError('已是"验证中"状态')
        else:
            raise UserError('不可以推到"验证中"状态')
    def action_set_Verified(self):
        if self.state =='In Verification':
            self.write({'state':'Verified'})
        elif self.state =='Verified':
            raise UserError('已是"已验证"状态')
        else:
            raise UserError('不可以推到"已验证"状态')
    def action_set_Closed(self):
        if self.state =='Verified':
            self.write({'state':'Closed'})          
        elif self.state =='Closed':
            raise UserError('已是"关闭"状态')          
        elif self.state =='Submitted':
            raise UserError('不可以推到"关闭"状态')          
        elif self.state =='In Verification':
            raise UserError('不可以推到"关闭"状态')        
        else:
            raise UserError('已取消,不能被关闭')
    def action_set_Cancel(self):
        if self.state =='Submitted':
            self.write({'state':'Cancel'})
        elif self.state =='In Verification':
            self.write({'state':'Cancel'}) 
        elif self.state =='Verified':
            self.write({'state':'Cancel'})             
        elif self.state =='Cancel':
            raise UserError('已是"取消"状态')
        else:
            raise UserError('已关闭,不能被取消')


 #增加欄位 2024.11.4 Herbert增加
    @api.model
    def get_tiles_data(self,data):
        # sources =self.search([('owner_id', '=' , self.env.user.id)])
        # source_customer=sources.filtered(lambda r: r.issue_Source == 'Customer')
        # source_internal=sources.filtered(lambda r: r.issue_Source == 'Internal')
        # source_supplier=sources.filtered(lambda r: r.issue_Source == 'Supplier')
        source_customer = self.env['issue'].search_count([('issue_Source', '=', 'Customer')])
        source_internal = self.env['issue'].search_count([('issue_Source', '=', 'Internal')])
        source_supplier = self.env['issue'].search_count([('issue_Source', '=', 'Supplier')])
        if data and data !='0' :
            start_date = datetime.now() - timedelta(days=int(data))
            source_customer = self.env['issue'].search_count([('issue_Source', '=', 'Customer'),('create_date','>=',start_date)])
            source_internal = self.env['issue'].search_count([('issue_Source', '=', 'Internal'),('create_date','>=',start_date)])
            source_supplier = self.env['issue'].search_count([('issue_Source', '=', 'Supplier'),('create_date','>=',start_date)])
        
        if not source_customer :
            source_customer=0
        if not source_internal :
            source_internal=0
        if not source_supplier :
            source_supplier=0
        
        return {
            'total_customer': source_customer,
            'total_internal': source_internal,
            'total_supplier': source_supplier,
        }
    
    @api.model
    def getpco_status_counts(self,data):         
        new_count=self.env['pco'].search_count([('state', '=', 'New')])
        review_count=self.env['pco'].search_count([('state', '=', 'Review')])
        approved_count= self.env['pco'].search_count([('state', '=', 'Approved')])
        cancel_count= self.env['pco'].search_count([('state', '=', 'Cancel')])
        if data and data !='0' :
            start_date = datetime.now() - timedelta(days=int(data))
            new_count=self.env['pco'].search_count([('state', '=', 'New'),('create_date','>=',start_date)])
            review_count=self.env['pco'].search_count([('state', '=', 'Review'),('create_date','>=',start_date)])
            approved_count= self.env['pco'].search_count([('state', '=', 'Approved'),('create_date','>=',start_date)])
            cancel_count= self.env['pco'].search_count([('state', '=', 'Cancel'),('create_date','>=',start_date)])
        
        if not new_count :
            new_count=0
        if not review_count :
            review_count=0
        if not approved_count :
            approved_count=0
        if not cancel_count :
            cancel_count=0
        return {
            'new_count': new_count,
            'review_count': review_count,
            'approved_count': approved_count,
            'cancel_count':  cancel_count
        }
        # data = [
        #     {'value': 335, 'name': '直接访问'},
        #     {'value': 310, 'name': '邮件营销'},
        #     {'value': 234, 'name': '联盟广告'},
        #     {'value': 135, 'name': '视频广告'},
        #     {'value': 1548, 'name': '搜索引擎'}
        # ]
        # return data
    @api.model
    def getdco_status_counts(self,data): 
        new_count=self.env['dco'].search_count([('state', '=', 'New')])
        review_count=self.env['dco'].search_count([('state', '=', 'Review')])
        approved_count= self.env['dco'].search_count([('state', '=', 'Approved')])
        cancel_count= self.env['dco'].search_count([('state', '=', 'Cancel')])
        if data and data !='0' :
            start_date = datetime.now() - timedelta(days=int(data))
            new_count=self.env['dco'].search_count([('state', '=', 'New'),('create_date','>=',start_date)])
            review_count=self.env['dco'].search_count([('state', '=', 'Review'),('create_date','>=',start_date)])
            approved_count= self.env['dco'].search_count([('state', '=', 'Approved'),('create_date','>=',start_date)])
            cancel_count= self.env['dco'].search_count([('state', '=', 'Cancel'),('create_date','>=',start_date)])
        if not new_count :
            new_count=0
        if not review_count :
            review_count=0
        if not approved_count :
            approved_count=0
        if not cancel_count :
            cancel_count=0
        return {
            'new_count': new_count,
            'review_count': review_count,
            'approved_count': approved_count,
            'cancel_count':  cancel_count
        }
    # 项目阶段数量统计
    @api.model
    def getprj_tag_counts(self,data):      
        domain = [('tag_ids','!=',''),('tag_ids', '!=', False)]  # 定义你的搜索过滤条件
        if data and data !='0' :
            start_date = datetime.now() - timedelta(days=int(data))
            domain=[('create_date','>=',start_date),('tag_ids','!=',''),('tag_ids', '!=', False)]
        ctagids_counts = self.env['project.project'].read_group(
            domain,
            ['tag_ids', 'id:sum'],  # 分组依据的字段
            ['tag_ids', 'count(id) as count'],  # 要统计的字段
            orderby='id:sum DESC',
            limit=5
        )
        return ctagids_counts
    
    # 任务状态数量统计
    @api.model
    def gettask_state_counts(self,data):      
        domain = [('project_id.last_update_status','not in',('off_track', 'to_define', 'to_define', 'done'))]  # 定义你的搜索过滤条件
        if data and data !='0' :
            start_date = datetime.now() - timedelta(days=int(data))
            domain=[('project_id.last_update_status','not in',('off_track', 'to_define', 'to_define', 'done')),('create_date','>=',start_date)]
        ctagids_counts = self.env['project.task'].read_group(
            domain,
            ['state'],  # 分组依据的字段
            ['state', 'count(id) as count']  # 要统计的字段
            
        )
        return ctagids_counts
    
    # issue tag
    @api.model
    def getisu_tag_counts(self,data):      
        domain = [('issue_code_ids', '!=', False), ('issue_code_ids', '!=', ''), ('issue_code_ids', '!=', (False, '')), ('issue_code_ids', '!=', None)] # 定义你的搜索过滤条件
        if data and data !='0' :
            start_date = datetime.now() - timedelta(days=int(data))
            domain=[('issue_code_ids', '!=', False), ('issue_code_ids', '!=', ''), ('issue_code_ids', '!=', (False, '')), ('issue_code_ids', '!=', None),('create_date','>=',start_date)]
        ctagids_counts = self.env['issue'].read_group(
            domain,
            ['issue_code_ids', 'id:sum'],  # 分组依据的字段
            ['issue_code_ids', 'count(id) as count'],   # 要统计的字段
            orderby='id:sum DESC',
            limit=5
        )
        return ctagids_counts

    # 统计问题单top 5最大的产品
    @api.model
    def getprdmaxiss_counts(self,data):
        domain = [('issue_product_id','!=',''),('issue_product_id', '!=', False)]
        if data and data !='0' :
            start_date = datetime.now() - timedelta(days=int(data))
            domain=[('create_date','>=',start_date),('issue_product_id','!=',''),('issue_product_id', '!=', False)]
        prdmaxids_counts = self.env['issue'].read_group(
            domain,
            ['issue_product_id', 'id:sum'],  # 分组依据的字段
            ['issue_product_id', 'count(id) as count'],  # 要统计的字段
            orderby='id:sum DESC',
            limit=5
        )
        return prdmaxids_counts


    # 统计dco tags tag_ids
    @api.model
    def getdco_tag_counts(self,data):      
        domain = [('tag_ids','!=',''),('tag_ids', '!=', False)]  # 定义你的搜索过滤条件
        if data and data !='0' :
            start_date = datetime.now() - timedelta(days=int(data))
            domain=[('create_date','>=',start_date),('tag_ids','!=',''),('tag_ids', '!=', False)]
        ctagids_counts = self.env['dco'].read_group(
            domain,
            ['tag_ids', 'id:sum'],  # 分组依据的字段
            ['tag_ids', 'count(id) as count'],  # 要统计的字段
            orderby='id:sum DESC',
            limit=5
        )
        return ctagids_counts
    # 统计dco tags tag_ids
    @api.model
    def getpco_tag_counts(self,data):      
        domain = [('tag_ids','!=',''),('tag_ids', '!=', False)]  # 定义你的搜索过滤条件
        if data and data !='0' :
            start_date = datetime.now() - timedelta(days=int(data))
            domain=[('create_date','>=',start_date),('tag_ids','!=',''),('tag_ids', '!=', False)]
        ctagids_counts = self.env['pco'].read_group(
            domain,
            ['tag_ids', 'id:sum'],  # 分组依据的字段
            ['tag_ids', 'count(id) as count'] ,  # 要统计的字段
            orderby='id:sum DESC',
            limit=5
        )
        return ctagids_counts



# class AttachmentUpload(http.Controller):
#     @http.route('/upload_attachments', type='http', methods=['POST'], auth='public', csrf=False)
#     def upload_attachments(self, model, id, **kwargs):
#         files = request.httprequest.files.getlist('files')
#         attachment_ids = []
#         for file in files:
#             attachment = request.env['ir.attachment'].create({
#                 'name': file.filename,
#                 'datas': file.read(),
#                 'res_model': model,
#                 'res_id': int(id),
#             })
#             attachment_ids.append(attachment.id)
#         return request.make_response("Files uploaded successfully", 200)