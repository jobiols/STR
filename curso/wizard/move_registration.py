# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import osv, fields


class curso_move_registration(osv.osv_memory):
    def button_move_registration(self, cr, uid, ids, context=None):
        reg_pool = self.pool['curso.registration']
        for wiz in self.browse(cr, uid, ids, context):
            # por cada inscripcion marcada cambiarle el curso
            for reg in reg_pool.browse(cr, uid, context['active_ids']):
                reg.curso_id = wiz.curso_id

    _name = "curso.move.registration"
    _description = "Mover inscripciones entre cursos"

    _columns = {
        'curso_id': fields.many2one('curso.curso', 'Curso', required=True),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
