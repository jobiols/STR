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
from openerp import models, fields, api
from datetime import datetime

class add_registration(models.TransientModel):
    """ Wizard para agregar una inscripción de una clienta a un curso """
    _name = 'curso.add_registration'
    _description = "Inscribir alumna en curso"

    curso_id = fields.Many2one(
        'curso.curso',
        string="Curso",
        required=True)
#        domain="[('begin_date','&gt;=',context_today())]")

    @api.one
    def button_add_curso(self):
        """ Agrega un curso a la ficha de la alumna, y la pone como interesada
        """
        #  obtener el id de la alumna que viene en el contexto
        partner_ids = self._context.get("active_ids")

        # Crear la inscripcion y agregarla
        vals = {
            'curso_id': self.curso_id.id,
            'partner_id': partner_ids[0],
            'user_id': self._uid
        }
        self.env['curso.registration'].create(vals)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
