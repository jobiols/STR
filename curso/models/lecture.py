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
from datetime import datetime, timedelta
from openerp.osv import fields, osv

class curso_lecture(osv.osv):
    """ Representa las clases del curso """
    _description = __doc__
    _name = 'curso.lecture'

    def _weekday(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for rec in self.browse(cr, uid, ids):
            ans = datetime.strptime(rec.date, '%Y-%m-%d')
            res[rec.id] = ans.strftime("%A")
        return res

    def _calc_datetime(self, _date, _time):

        dt = datetime.strptime(_date, "%Y-%m-%d")

        mm = _time - int(_time)
        hh = int(_time - mm)
        mm = int(mm * 60)

        tt = datetime(dt.year, dt.month, dt.day, hh, mm, tzinfo=None)

        # TODO aca sumamos tres horas porque inexplicablemente al mostrar
        # el campo le resta tres horas.
        tt = tt + timedelta(hours=3)
        b = tt.strftime("%Y-%m-%d %H:%M:%S")

        return b

    def _get_start(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for rec in self.browse(cr, uid, ids):
            res[rec.id] = self._calc_datetime(rec.date, rec.schedule_id.start_time)
        return res

    def _get_stop(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for rec in self.browse(cr, uid, ids):
            res[rec.id] = self._calc_datetime(rec.date, rec.schedule_id.end_time)
        return res

    _columns = {
        'date': fields.date('Fecha'),
        'desc': fields.text('Descripcion'),
        'curso_id': fields.many2one('curso.curso', 'Curso', readonly=False,
                                    required=True,
                                    help='Curso al que pertenece esta clase'),
        'curso_child_id': fields.many2one('curso.curso', 'Hijo', readonly=False,
                                          domain="[('child','=',True)]",
                                          help='Curso hijo que se inserta en este'),
        'schedule_id': fields.many2one('curso.schedule', 'Horario', readonly=False,
                                       required=True),
        'weekday': fields.function(_weekday, string="Dia", type="char", method=True),
        'date_start': fields.function(_get_start, string="Inicio de clase",
                                      type="datetime", method=True),
        'date_stop': fields.function(_get_stop, string="Fin de clase", type="datetime",
                                     method=True),
    }

    # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
