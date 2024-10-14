from odoo import api,fields, models,_

class InhtBOMtModel(models.Model):
    _inherit = 'mrp.bom'

    item_number = fields.Char(string="編號",default=lambda self:_("no"),copy=False,readonly=True)
    xbom_type   = fields.Selection([('E', 'EBOM'), ('M', 'MBOM')], string='BOM類型')

    cnis_current = fields.Boolean('isCurrent', default=True,readonly=True)
    cn_configid = fields.Char(string='configid',default="0",readonly=True)
    version = fields.Integer('Version', default=1, readonly=True)

    state = fields.Selection([
            ('Draft', 'Draft'),
            ('Review', 'Review'),
            ('Released', 'Released'),
            ('InChange', 'InChange'),
            ('Superseded', 'Superseded')],string = "狀態",
            copy=False, default='Draft', readonly=True, required=True, index=True)

    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            if vals.get('item_number',_('no'))== _('no'):
                vals['item_number'] =self.env['ir.sequence'].next_by_code('mrpbom')
                #return super().create(vals_list)
                res = super(InhtBOMtModel, self).create(vals_list)
                if  res.cn_configid =="0"  :
                    res.write({'cn_configid': res.id})
                return res
    
    #ebert按钮跳转页面    
    def action_open_versions(self): 
        return {
        'name': '历程记录',
        'res_model': 'mrp.bom', 
        'view_mode': 'tree,form',
        'domain': [('active', '=', False),('product_tmpl_id', '=', self.product_tmpl_id.id)],
        'type': 'ir.actions.act_window',
        }


