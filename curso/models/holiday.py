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
from openerp import models, fields

class curso_holiday(models.Model):
    #class curso_holiday(models.Model):
    """ define los periodos donde estamos en vacaciones, puede ser parte de un dia """
    _name = 'curso.holiday'
    _inherit = 'curso.lapse'

    name = fields.Char(string='Nombre')
    date = fields.Date(string='Fecha')
    start_time = fields.Float(default=8)
    end_time = fields.Float(default=22)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: