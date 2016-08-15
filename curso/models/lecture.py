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
from datetime import datetime
from openerp import models, fields, api

class curso_lecture(models.Model):
    """ Representa las clases del curso """
    _name = 'curso.lecture'

    name = fields.Text(
        'Contenido de la clase')

    date = fields.Date(
        'Fecha')

    curso_id = fields.Many2one(
        'curso.curso', string='Curso', required=True,
        help='Curso al que pertenece esta clase')

    schedule_id = fields.Many2one(
        'curso.schedule', string='Horario programado',
        required=True,
        help='Horario original de la clase')

    weekday = fields.Char(
        compute="_weekday", string="Dia")

    date_start = fields.Datetime(
        string="Inicio de clase")

    date_stop = fields.Datetime(
        string="Fin de clase")

    seq = fields.Integer(
        'Número de clase')

    @api.one
    def _weekday(self):
        ans = datetime.strptime(self.date, '%Y-%m-%d')
        self.weekday = ans.strftime("%A").capitalize()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
