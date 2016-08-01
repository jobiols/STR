# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------------
from openerp import fields, models, api


class mail_confirm(models.TransientModel):
    """Mail Confirmation"""
    _name = "curso.mail.confirm"

    registration_ids = fields.One2many(
        'curso.registration', 'curso_id', u'Inscripciones',
        domain=[],
        readonly=True)

    @api.multi
    def confirm(self):
        print '------------',self._context.get('curso_id', False)
#        events = self.env['event.event'].browse(self._context.get('event_ids', []))
#        events.do_confirm()
        return {'type': 'ir.actions.act_window_close'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
