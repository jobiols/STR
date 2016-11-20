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
from openerp import models, fields, api
from datetime import datetime, timedelta

class curso_schedule(models.Model):
    """ horarios que puede tener un curso """
    _name = 'curso.schedule'
    _inherit = 'curso.lapse'
    _sql_constraints = [
        ('default_code_unique', 'unique (name)', 'Este horario ya existe.')]

    name = fields.Char(
        compute="_get_name",
        store=True
    )

    @api.one
    def _calc_datetime(self, _date, _time):

        mm = _time - int(_time)
        hh = int(_time - mm)
        mm = int(mm * 60)

        tt = datetime(_date.year, _date.month, _date.day, hh, mm, tzinfo=None)

        # aca sumamos tres horas porque es UTC
        # el campo le resta tres horas.
        tt = tt + timedelta(hours=3)
        b = tt.strftime("%Y-%m-%d %H:%M:%S")

        return b

    def start_datetime(self,date):
        return self._calc_datetime(date, self.start_time)

    def stop_datetime(self,date):
        return self._calc_datetime(date, self.end_time)

    def _f2h(self, t):
        mm = t - int(t)
        hh = t - mm
        return "{:0>2d}:{:0>2d}".format(int(hh), int(mm * 60))

    def _f2hh_mm(self, t):
        mm = t - int(t)
        hh = t - mm
        mm *= 60
        if int(mm) == 0:
            res = "{}hs".format(int(hh))
        else:
            res = "{}hs {}min".format(int(hh), int(mm))
        return res

    @api.one
    @api.depends('start_time','end_time')
    def _get_name(self):
        aa = self._f2h(self.start_time)
        bb = self._f2h(self.end_time)
        cc = self._f2hh_mm(self.end_time - self.start_time)
        self.name = "{} - {} ({})".format(aa, bb, cc)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: