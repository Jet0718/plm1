from odoo import api,fields, models,_

from odoo.exceptions import UserError

class InhtProjectModel(models.Model):
    _name = "ir.attachment"
    _description="Ir Attachment"
    _inherit = ['revision.plm.mixin', 'ir.attachment']    
    
    #ebert
    # item_number = fields.Char(string="編號",default=lambda self:_("no"),copy=False,readonly=True)
    # version =fields.Integer(string ="版本",default=1,readonly=True)
    active = fields.Boolean(string ="启用",default=True,readonly=True)
    owner=fields.Many2one('res.users', default=lambda self: self.env.user.id, string="責任人")
    contactor =fields.Many2one('res.partner', string="聯絡人")
    # state = fields.Selection([
    #         ('Draft', 'Draft'),
    #         ('Review', 'Review'),
    #         ('Released', 'Released'),
    #         ('InChange', 'InChange'),
    #         ('Superseded', 'Superseded')],string = "狀態",
    #         copy=False, default='Draft',  required=True, index=True)
    cnis_current = fields.Boolean('isCurrent', default=True,readonly=True)
    cn_configid = fields.Char(string='configid',default="0",copy=False,readonly=True)

    cn_file2prj = fields.Many2many('project.project',string='项目')

    cn_file2prd = fields.Many2many('product.template',string='产品')


    # cn_file2prj = fields.One2many('project.project','cn_prj2file1',string='项目')
    cn_cadfile_ships = fields.One2many('ir.attachment.ships','iship_id','子阶图纸')




    @api.model_create_multi
    def create(self, vals_list):
        new_vals_list = []
        for vals in vals_list:           
            #ebert
            # if vals.get('item_number',_('no'))== _('no'):
            #     vals['item_number'] =self.env['ir.sequence'].next_by_code('dmsdocument')
            
            if not vals.get('engineering_code'):
                # raise UserError(self.env['ir.sequence'].next_by_code('irattachmen_seq'))
                vals['engineering_code'] =self.env['ir.sequence'].next_by_code('irattachmenseq')
                vals['cn_configid'] = vals.get('id')
            new_vals_list.append(vals)
        return super().create(new_vals_list)
    
    #ebert按钮跳转页面    
    def action_openfileversions(self): 
         return {
            'name': '历程记录',
            'res_model': 'ir.attachment', 
            'view_mode': 'tree,form',
            #'view_id': self.env.ref('product.template.product_template_tree_view').id,   
            'domain': [('active', '=', False),('cn_configid', '=', self.cn_configid)],  
            #'context': {'search_default_group': 'my_group'},
            'type': 'ir.actions.act_window',
        }
  




            

