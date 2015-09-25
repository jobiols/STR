# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution.
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>...
#
##############################################################################
from openerp.osv import fields, osv


class add_registration(osv.osv_memory):
    """ Wizard para agregar una inscripción de una clienta a un curso """

    def button_add_curso(self, cr, uid, ids, context=None):
        """ Agrega un curso a la ficha de la alumna, y la pone como interesada
        """
        #  obtener el id de la alumna que esta en el contexto
        ids_alumna = context.get("active_ids")

        # Obtener el id del curso donde inscribir la alumna
        pool = self.pool.get('curso.add_registration')
        for reg in pool.browse(cr, uid, ids, context):
            curso_id = reg.curso_id.id

        # Crear la la inscripcion y agregarla
        registration_data = {
            'curso_id': curso_id,
            'partner_id': ids_alumna[0],
            'user_id': uid
        }
        self.pool.get('curso.registration').create(cr, uid, registration_data,
                                                   context=context)

        return True

    _name = 'curso.add_registration'
    _description = "Inscribir alumna en curso"

    _columns = {
        'curso_id': fields.many2one('curso.curso', 'Curso', required=True,
                                    readonly=False),
    }
