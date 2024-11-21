##############################################################################
#
#    OmniaSolutions, Your own solutions
#    Copyright (C) 2010 OmniaSolutions (<https://www.omniasolutions.website>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import logging
from odoo import _
from odoo import api
from odoo import models
from odoo import fields


class PlmDocumentRelations(models.Model):
    _name = 'ir.attachment.ships'
    _description = "Relation between document used for cad file structure"
    # _inherit = ['ir.attachment.relation'] 
    
   
    iship_id = fields.Many2one('ir.attachment', 'attachment',required=True)

    irattachment_id = fields.Many2one('ir.attachment', 'attachment',required=True,domain="['&',('engineering_code', '!=', ''),('url', '=', False),('engineering_state', 'not in', ['obsoleted','undermodify'])]")

    engineering_code = fields.Char(related="irattachment_id.engineering_code",string="item_number")
    engineering_revision = fields.Integer(related="irattachment_id.engineering_revision",string="revision")
    name = fields.Char(related="irattachment_id.name",string="name")
    type = fields.Selection(related="irattachment_id.type",string="type")
    preview = fields.Image(related="irattachment_id.preview")
    # preview = fields.Image(_('Preview Content'),
    #                        max_width=1920,
    #                        max_height=1920,
    #                        attachment=False)