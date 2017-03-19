# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------------
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
# -----------------------------------------------------------------------------------
from datetime import datetime

from openerp import models, fields, api


class curso_assistance(models.Model):
    """ Modelo para manejar asistencias a clase """

    _name = 'curso.assistance'
    _description = __doc__
    _sql_constraints = [
        ('unique_partner_per_class', 'unique (lecture_id, partner_id, date)',
         'Una alumna no puede aparecer dos veces en una clase')]

    future = fields.Boolean(
            'Futuro',
            help=u'La fecha de la clase está en el futuro',
            compute='_get_future'
    )
    lecture_id = fields.Many2one(
            'curso.lecture',
            string='Clase',
            help=u'Clase a la que pertenece este registro de asistencia'
    )
    seq = fields.Integer(
            'Clase',
            related='lecture_id.seq',
            store=False)

    partner_id = fields.Many2one(
            'res.partner',
            required=True,
            string=u'Alumna',
            help=u'Alumna a la que pertenece este registro de asistencia'
    )
    state = fields.Selection([
        ('programmed', 'Programado'),
        ('absent', 'Ausente'),
        ('present', 'Presente'),
        ('abandoned', 'Abandonado')
    ])
    present = fields.Boolean(
            'Presente',
            compute='_get_present',
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

    date = fields.Date(
            related='lecture_id.date'
    )

    curso_instance = fields.Char(
            related='lecture_id.curso_id.curso_instance'
    )

    @api.multi
    def button_present(self):
        """ La profesora le pone o le saca el presente a la alumna """
        for reg in self:
            reg.present = not reg.present

    @api.multi
    @api.depends('partner_id')
    def _get_info(self):
        for rec in self:
            rec.info = rec.partner_id.get_info()

    @api.multi
    @api.depends('state')
    def _get_present(self):
        for rec in self:
            rec.present = rec.state == 'present'

    @api.multi
    def button_go_absent(self):
        """ La alumna informa que no va a venir a esta clase """
        for rec in self:
            rec.state = 'absent'

    @api.multi
    def button_go_programmed(self):
        """ La alumna informa que no va a venir a esta clase """
        for rec in self:
            rec.state = 'programmed'

    @api.multi
    @api.depends('date')
    def _get_future(self):
        for rec in self:
            rec.future = datetime.today() < datetime.strptime(rec.date, '%Y-%m-%d')

    @api.multi
    def get_recover_ids(self, partner_id):
        """ dada una alumna devolver los ids de las clases de recuperatorio """

        print '-----------------------------------------------------------------------------------'

        # averiguar a que clases faltó esta alumna
        absent_lectures = self.search([('partner_id', '=', partner_id),
                                       ('state', '=', 'absent')])

        for al in absent_lectures:
            print 'falto a ',al.lecture_id.default_code, al.seq

        print '-----------------------------------------------------------------------------------'


        # obtener los cursos y clases que necesita recuperar
        lectures_obj = self.env['curso.lecture']
        ret = []
        for al in absent_lectures:
            default_code = al.lecture_id.curso_id.default_code  # que curso tiene que recuperar
            seq = al.lecture_id.seq  # que numero de clase tiene que recuperar

            print 'necesita recuperar', default_code, seq


            # averiguar que clases hay para ese curso y numero de clase
            candidate_lectures = lectures_obj.search([('default_code', '=', default_code),
                                                      ('seq', '=', seq),
                                                      ('next', '=', True)])


            for cl in candidate_lectures:
                print 'candidatos', cl.id, cl.default_code, cl.seq, cl.name
                ret.append(cl.id)

        print 'devolviendo',ret

        return ret

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
