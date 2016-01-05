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


class curso_diary(osv.osv):
    """ relaciona un horario con un dia de la semana
    """
    _name = 'curso.diary'

    _columns = {
        'weekday': fields.integer('Dia',
                                  readonly=False),
        'schedule': fields.many2one('curso.schedule',
                                    'Horario',
                                    readonly=False),
        'seq': fields.integer('secuencia')
    }

    # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
