from odoo import api,fields, models,_

class InhtProjectTaskModel(models.Model):
    _inherit = "project.task" 



    cnprjtask_file = fields.Many2many('dms.file', string= '工程文件')




  




            

