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
    _order = 'seq'

    def _get_day_name(self, cr, uid, ids, fields, args, context=None):
        dwd = {
            '0': u'Domingo',
            '1': u'Lunes',
            '2': u'Martes',
            '3': u'Miércoles',
            '4': u'Jueves',
            '5': u'Viernes',
            '6': u'Sábado'
        }

        res = {}
        for diary in self.browse(cr, uid, ids, context=context):
            res[diary.id] = dwd[diary.weekday]
        return res

    def _get_day(self, cursor, user_id, context=None):
        return (
            ('0', u'Domingo'),
            ('1', u'Lunes'),
            ('2', u'Martes'),
            ('3', u'Miércoles'),
            ('4', u'Jueves'),
            ('5', u'Viernes'),
            ('6', u'Sábado')
        )

    _columns = {
        'curso_id': fields.many2one('curso.curso',
                                    u'Curso',
                                    readonly=False),
        'weekday': fields.selection(_get_day,
                                    u'Día',
                                    readonly=False,
                                    required=True,
                                    track_visibility='onchange'),
        'weekday_name': fields.function(_get_day_name, fnct_search=None,
                                        string='Nombre del dia',
                                        method=True, store=True,
                                        type='char'),


        'schedule': fields.many2one('curso.schedule',
                                    u'Horario',
                                    readonly=False),
        'seq': fields.integer('Secuencia')
    }

    # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
