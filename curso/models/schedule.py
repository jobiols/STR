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

class curso_schedule(osv.osv):
    """ horarios que puede tener un curso """
    _name = 'curso.schedule'
    _inherit = 'curso.lapse'

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

    def _get_name(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for shedule in self.browse(cr, uid, ids, context=context):
            aa = self._f2h(shedule.start_time)
            bb = self._f2h(shedule.end_time)
            cc = self._f2hh_mm(shedule.end_time - shedule.start_time)
            name = "{} - {} ({})".format(aa, bb, cc)
            res[shedule.id] = name
        return res

    _columns = {
        'name': fields.function(_get_name, fnct_search=None, string='Nombre del horario',
                                method=True, store=True,
                                type='char'),
    }

    _sql_constraints = [
        ('default_code_unique', 'unique (name)', 'Este horario ya existe.')]

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: