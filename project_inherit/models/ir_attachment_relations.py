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
    _inherit = 'ir.attachment.relation'
    _description = "Relation between document used for cad file structure"
    # _inherit = ['ir.attachment.relation'] 
    
   
    ir_attachment_relations       = fields.One2many('ir_attachment_relation.ship', 'prd_id', '規格特性')




class irattachmentrelationShip(models.Model):
    _name="ir_attachment_relation.ship"
    _description="ir.attachment.relations ship"

    prd_id=fields.Many2one('ir.attachment.relation',"relation Doc",required=True)

    
    
    child_id = fields.Many2one('ir.attachment',
                               _('Related child document'),
                               ondelete='cascade',
                               index=True)
    
    child_preview = fields.Binary(related="child_id.preview",
                                  string=_("Child Preview"),
                                  store=False)
    child_state = fields.Selection(related="child_id.engineering_state",
                                   string=_("Child Status"),
                                   store=False)
    child_revision = fields.Integer(related="child_id.engineering_revision",
                                    string=_("Child Revision"),
                                    store=False)
    child_linked = fields.Boolean(related="child_id.is_linkedcomponents",
                                    string=_("Child Linked Components"),
                                    store=False)
    child_type = fields.Selection(related="child_id.document_type",
                                    string=_("Child Document Type"),
                                    store=False)
    parent_id = fields.Many2one('ir.attachment',
                                _('Related parent document'),
                                ondelete='cascade',
                                index=True,)