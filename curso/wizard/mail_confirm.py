# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------------
#
#    Copyright (C) 2016  jeo Software  (http://www.jeo-soft.com.ar)
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# -----------------------------------------------------------------------------------
from openerp import fields, models, api

class mail_confirm(models.TransientModel):
    """Mail Confirmation"""
    _name = "curso.mail.confirm"

    mails_ids = fields.Many2many(
        comodel_name='curso.registration')

    # este campo esta solo para que funcione el onchange
    reset_mails = fields.Boolean()

    # el onchange hace que se carge al iniciar del wizard
    @api.onchange('reset_mails')
    @api.multi
    def reset(self):
        curso_id = self._context.get('curso_id', False)
        reg_obj = self.env['curso.registration'].search([('curso_id', '=', curso_id)])
        for reg in reg_obj:
            self.mails_ids += reg

    @api.multi
    def confirm(self):
        """ Intentar enviar mail a todas las alumnas que tengo
        """
        for reg in self.mails_ids:
            reg.try_send_mail_by_lecture()



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
