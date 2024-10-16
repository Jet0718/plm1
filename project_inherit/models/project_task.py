from odoo import api,fields, models,_

# from dms_file import InhtProjectModel

from odoo.exceptions import UserError, ValidationError
class InhtProjectModel(models.Model):
    _inherit = "dms.file"    
    
    #ebert
    item_number = fields.Char(string="編號",default=lambda self:_("no"),copy=False,readonly=True)
    version =fields.Integer(string ="版本",default=1,readonly=True)
    active = fields.Boolean(string ="启用",default=True,readonly=True)
    owner=fields.Many2one('res.users', default=lambda self: self.env.user.id, string="責任人")
    contactor =fields.Many2one('res.partner', string="聯絡人")
    state = fields.Selection([
            ('Draft', 'Draft'),
            ('Review', 'Review'),
            ('Released', 'Released'),
            ('InChange', 'InChange'),
            ('Superseded', 'Superseded')],string = "狀態",
            copy=False, default='Draft',  required=True, index=True)
    cnis_current = fields.Boolean('isCurrent', default=True,readonly=True)
    cn_configid = fields.Char(string='configid',default="0",copy=False,readonly=True)

    # cn_prj2file =fields.Many2one('dms.file', 'file', ondelete='cascade')
    cn_file2prj = fields.Many2many('project.project',string='项目')

    cn_file2prd = fields.Many2many('product.template',string='产品')


    # cn_file2prj = fields.One2many('project.project','cn_prj2file1',string='项目')




    @api.model_create_multi
    def create(self, vals_list):
        new_vals_list = []
        for vals in vals_list:           
            #ebert
            if vals.get('item_number',_('no'))== _('no'):
                vals['item_number'] =self.env['ir.sequence'].next_by_code('dmsdocument')
            new_vals_list.append(vals)
        return super().create(new_vals_list)
    







class InhtProjectTaskModel(models.Model):
    _inherit = "project.task" 



    cnprjtask_file = fields.Many2many('dms.file', string= '工程文件',ondelete ='cascade')


    # def write(self, vals):
    #     # 在更新記錄時，添加新的 Many2many 關係
    #     if 'cnprjtask_file' in vals:
    #         # ... 處理新增的 Many2many 關係
    #         self.cnprjtask_file.write({'cn_file2prj': self.project_id})


    @api.onchange('cnprjtask_file')
    def _onchange_cnprjtask_file(self):
        # raise UserError("test")
        new_values = self.cnprjtask_file.ids
        old_values = self._context.get('old_cnprjtask_file', [])
        added_records = set(new_values) - set(old_values)
        for record in added_records:
            if  self.project_id:
                f =self.env['dms.file'].search([('id', '=', record)])
                if f :                    
                    # (0, 0, values): 創建一條新記錄並添加到 Many2many 字段中。
                    # 0: 表示創建新記錄。
                    # 0: 表示不指定 ID（系統會自動分配）。
                    # values: 新記錄的字段值。
                    # (1, id, values): 更新一個已存在的記錄。
                    # 1: 表示更新記錄。
                    # id: 要更新記錄的 ID。
                    # values: 更新的值。
                    # (2, id): 刪除一個記錄。
                    # 2: 表示刪除記錄。
                    # id: 要刪除記錄的 ID。
                    # (3, id): 從 Many2many 關係中移除一個記錄，但不刪除該記錄。
                    # 3: 表示從關係中移除。
                    # id: 要移除記錄的 ID。
                    # (4, id): 將一個已存在的記錄添加到 Many2many 關係中。
                    # 4: 表示添加到關係中。
                    # id: 要添加記錄的 ID。
                    # (5,): 刪除 Many2many 關係中的所有記錄。
                    # (6, 0, [ids]): 替換 Many2many 關係中的所有記錄。
                    # 6: 表示替換。
                    # 0: 表示不創建新記錄。
                    # [ids]: 要替換成的記錄 ID 列表。            
                    f.write({'cn_file2prj': [(4,self.project_id.id)]})

        

        # 獲取原始的 Many2many 數據
        original_values = self._origin.cnprjtask_file.ids
        # 獲取新的 Many2many 數據
        new_values = self.cnprjtask_file.ids
        if len(self.cnprjtask_file.ids) == 0 :
            new_values = []

        # 計算被移除的數據
        removed_ids = set(original_values) - set(new_values)
        # 處理被移除的數據
        for record in removed_ids:
            if  self.project_id:
                f =self.env['dms.file'].search([('id', '=', record)])
                if f :      
                   f.write({'cn_file2prj': [(3, self.project_id.id)]})   
        