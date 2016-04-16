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
from openerp import models, fields, api

class curso_lecture(models.Model):
    """ Representa las clases del curso """
    _name = 'curso.lecture'

    @api.one
    def _weekday(self):
        ans = datetime.strptime(self.date, '%Y-%m-%d')
        self.weekday = ans.strftime("%A").capitalize()

    @api.one
    def _get_start(self):
        self.date_start = self._calc_datetime(self.date, self.schedule_id.start_time)

    @api.one
    def _get_stop(self):
        self.date_stop = self._calc_datetime(self.date, self.schedule_id.end_time)

    name = fields.Text('Contenido de la clase')
    date = fields.Date('Fecha')
    curso_id = fields.Many2one('curso.curso', string='Curso', required=True,
                               help='Curso al que pertenece esta clase')
    schedule_id = fields.Many2one('curso.schedule', string='Horario', required=True,
                                  help='Horario de la clase')
    weekday = fields.Char(compute=_weekday, string="Dia")
    date_start = fields.Datetime(compute=_get_start, string="Inicio de clase")
    date_stop = fields.Datetime(compute=_get_stop, string="Fin de clase")

    @api.one
    def _calc_datetime(self, _date, _time):

        dt = datetime.strptime(_date, "%Y-%m-%d")

        mm = _time - int(_time)
        hh = int(_time - mm)
        mm = int(mm * 60)

        tt = datetime(dt.year, dt.month, dt.day, hh, mm, tzinfo=None)

        # TODO aca sumamos tres horas porque es UTC
        # el campo le resta tres horas.
        tt = tt + timedelta(hours=3)
        b = tt.strftime("%Y-%m-%d %H:%M:%S")

        return b

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
