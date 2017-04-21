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
    """ Representa las clases de una instancia curso """

    _name = 'curso.lecture'
    _rec_name = 'name_list'
    _order = 'date_start'

    name_list = fields.Char(
            compute='_get_name_list'
    )
    name = fields.Text(
            'Contenido de la clase'
    )
    date = fields.Date(
            'Fecha',
            store="True",
            compute="_get_date"
    )
    curso_id = fields.Many2one(
            'curso.curso',
            string='Curso',
            help='Curso al que pertenece esta clase',
            required=True
    )
    schedule_id = fields.Many2one(
            'curso.schedule',
            string='Horario programado',
            help='Horario original de la clase',
            required=True
    )
    weekday = fields.Char(
            compute="_get_weekday",
            string="Dia"
    )
    date_start = fields.Datetime(
            string="Inicio de clase",
            required=True
    )
    date_stop = fields.Datetime(
            string="Fin de clase",
            required=True
    )
    seq = fields.Integer(
            'Número de clase',
            required=True
    )
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
    reg_max = fields.Integer(
            'Max',
            related="curso_id.register_max",
            help=u"La cantidad máxima alumnas que puede contener esta clase"
    )
    reg_recover = fields.Integer(
            'Recuperatorio',
            compute="_get_reg_vacancy",
            help=u"La cantidad de alumnas anotadas en esta clase para recuperar"
    )
    reg_absent = fields.Integer(
            'Ausente',
            compute="_get_reg_vacancy",
            help=u"La cantidad de alumnas que sabemos que no van a venir porque lo informaron"
    )
    reg_vacancy = fields.Integer(
            'Vacantes',
            compute="_get_reg_vacancy",
            help=u"La cantidad de vacantes reales teniendo en cuenta las que recuperan y las que "
                 u"avisan que no van a venir"
    )
    reg_virtual = fields.Integer(
            'Total real',
            compute="_get_reg_vacancy",
            help=u"La cantidad total de alumnas reales que hay"
    )

    @api.multi
    @api.depends('reg_max', 'reg_current', 'assistance_id')
    def _get_reg_vacancy(self):
        """ Calcula cantidades de alumnas

            Las que recuperan son las que tienen el tilde de recover y estan en programmed.
            si no están en programmed es porque avisaron que no van a vernir y las pasamos
            a absent.

            Las que estan absent son las que estan en estado absent.
        """
        for rec in self:
            reg_recover = rec.assistance_id.search_count([
                ('lecture_id', '=', rec.id),
                ('recover', '=', True),
                ('state', '=', 'programmed')
            ]
            )
            reg_absent = rec.assistance_id.search_count([
                ('lecture_id', '=', rec.id),
                ('state', '=', 'absent')]
            )

            rec.reg_recover = reg_recover
            rec.reg_absent = reg_absent
            rec.reg_virtual = rec.reg_current + reg_recover - reg_absent
            rec.reg_vacancy = rec.reg_max - rec.reg_current - reg_recover + reg_absent

    @api.multi
    def _get_name_list(self):
        for rec in self:
            rec.name_list = '{} [{}] - clase {} - conf {} - recu {} - ause {} - vac {} -- {}'.format(
                    datetime.strptime(rec.date, '%Y-%m-%d').strftime('%d/%m/%Y'),
                    rec.curso_id.curso_instance,
                    rec.seq,
                    rec.reg_current,
                    rec.reg_recover,
                    rec.reg_absent,
                    rec.reg_vacancy,
                    rec.name
            )

    @api.multi
    @api.depends('date_start')
    def _get_date(self):
        for rec in self:
            dt = datetime.strptime(rec.date_start, '%Y-%m-%d %H:%M:%S')
            rec.date = dt.strftime('%Y-%m-%d')

    @api.multi
    @api.depends('date')
    def _get_weekday(self):
        for rec in self:
            ans = datetime.strptime(rec.date, '%Y-%m-%d')
            rec.weekday = ans.strftime("%A").capitalize()

    @api.multi
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

        for rec in self:
            # Alumnas registradas en el curso
            atendees = rec.curso_id.registration_ids.search(
                    [('state', 'in', ['confirm', 'signed', 'done']),
                     ('curso_id', '=', rec.curso_id.id)]
            )

            # Alumnas en la lista de presentes, que no son recuperantes
            presents = rec.assistance_id.search(
                    [('lecture_id', '=', rec.id),
                     ('recover', '=', False)])

            for atendee in atendees:
                # Si el atendee no está en los presentes, incluirlo.
                if not contains(presents, atendee):
                    rec.assistance_id.add_atendee(atendee.partner_id, rec)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
