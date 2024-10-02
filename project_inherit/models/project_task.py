from odoo import api,fields, models,_

# from dms_file import InhtProjectModel


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



    cnprjtask_file = fields.Many2many('dms.file', string= '工程文件')



  




            

