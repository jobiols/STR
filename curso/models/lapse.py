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


class curso_lapse(osv.osv):
    """ Define un lapso de tiempo se usa como clase abstracta """
    _name = 'curso.lapse'
    _description = __doc__

    #   def _check_elapsed(self, cr, uid, ids, context=None):
    #        for curso in self.browse(cr, uid, ids, context=context):
    #            if curso.date_end < curso.date_begin:
    #                return False
    #        return True

    def _elapsed_time(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for rec in self.browse(cr, uid, ids):
            res[rec.id] = rec.end_time - rec.start_time
        return res

    _columns = {
        'start_time': fields.float('Desde', required=True),
        'end_time': fields.float('Hasta', required=True),
        'elapsed_time': fields.function(_elapsed_time, string="Duración", type="float",
                                        method=True)
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: