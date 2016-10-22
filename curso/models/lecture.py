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
        'Fecha',
        store="True",
        compute="_get_date")

    curso_id = fields.Many2one(
        'curso.curso', string='Curso',
        required=True,
        help='Curso al que pertenece esta clase',
    )

    schedule_id = fields.Many2one(
        'curso.schedule', string='Horario programado',
        required=True,
        help='Horario original de la clase')

    weekday = fields.Char(
        compute="_get_weekday", string="Dia")

    date_start = fields.Datetime(
        string="Inicio de clase")

    date_stop = fields.Datetime(
        string="Fin de clase")

    seq = fields.Integer(
        'Número de clase')

    assistance_id = fields.One2many(
        'curso.assistance',
        'lecture_id'
    )

    default_code = fields.Char(
        related="curso_id.default_code"
    )

    next = fields.Boolean(
        related="curso_id.next"
    )

    reg_current = fields.Integer(
        'Conf',
        related="curso_id.register_current",
        help=u"La cantidad de alumnas que confirmaron pagando (al menos una seña)"
    )
    reg_recover = fields.Integer(
        'Recu',
        compute="get_reg_recover",
        help=u"La cantidad de alumnas anotadas en esta clase para recuperar)"
    )

    @api.one
    @api.depends('assistance_id')
    def get_reg_recover(self):
        """ Calcular la cantidad de alumnas que recuperan en esta clase
        """
        #        self.reg_recover = self.env['curso.assistance'].search_count(
        self.reg_recover = self.assistance_id.search_count(
            [
                ('lecture_id', '=', self.id),
                ('recover', '=', True)
            ]
        )

    @api.one
    @api.depends('date_start')
    def _get_date(self):
        dt = datetime.strptime(self.date_start, '%Y-%m-%d %H:%M:%S')
        self.date = dt.strftime('%Y-%m-%d')

    @api.one
    @api.depends('date')
    def _get_weekday(self):
        ans = datetime.strptime(self.date, '%Y-%m-%d')
        self.weekday = ans.strftime("%A").capitalize()

    @api.one
    def button_generate_assistance(self):
        """ Pone en el registro de asistencia las alumnas que están cursando, que van a
            cursar o por las dudas también las que cumplieron en curso.
        """

        def contains(presents, atendee):
            """ Verifica si atendee está contenido en presents
            """
            ret = False
            for present in presents:
                if present.partner_id.id == atendee.partner_id.id:
                    ret = True
            return ret

        # Alumnas registradas en el curso
        atendees = self.curso_id.registration_ids.search(
            [('state','in',['confirm','signed','done']),
             ('curso_id','=',self.curso_id.id)]
        )

        # Alumnas en la lista de presentes, que no son recuperantes
        presents = self.assistance_id.search(
            [('lecture_id', '=', self.id),
             ('recover', '=', False)])

        for atendee in atendees:
            # Si el atendee no está en los presentes, incluirlo.
            if not contains(presents, atendee):
                self.assistance_id.create({
                    'lecture_id': self.id,
                    'present': False,
                    'recover': False,
                    'partner_id': atendee.partner_id.id
                })

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
