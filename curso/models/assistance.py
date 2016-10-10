# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------
#
#    Copyright (C) 2016  jeo Software  (http://www.jeo-soft.com.ar)
#    All Rights Reserved.
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
#-----------------------------------------------------------------------------------
from openerp import models, fields, api

class curso_assistance(models.Model):
    _name = 'curso.assistance'
    _sql_constraints = [
        ('unique_partner_per_class', 'unique (lecture_id, partner_id)',
         'No puede estar dos veces la misma alumna en la clase')]

    lecture_id = fields.Many2one(
        'curso.lecture',
        string='Clase',
        help=u'Clase a la que pertenece este registro de asistencia'
    )
    partner_id = fields.Many2one(
        'res.partner',
        required=True,
        string=u'Alumna'
    )
    present = fields.Boolean(
        'Presente',
        help=u'Tildado si la alumna estuvo presente en la clase'
    )
    recover = fields.Boolean(
        'Recupera',
        help=u'Tildado si la alumna está recuperando'
    )
    info = fields.Char(
        'Detalles',
        compute="_get_info",
        help=u'Información adicional'
    )

    @api.multi
    def button_present(self):
        """ La profesora le pone o le saca el presente a la alumna
        """
        for reg in self:
            reg.present = not reg.present

    @api.one
    @api.depends('partner_id')
    def _get_info(self):
        self.info = self.partner_id.get_info()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
