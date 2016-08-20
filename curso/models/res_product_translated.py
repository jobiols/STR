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
from openerp import models, fields, api
from openerp.exceptions import ValidationError
from datetime import datetime

class product_template(models.Model):
    _inherit = 'product.template'
    type = fields.Selection(selection_add=[('curso', 'Curso')])


class product_product(models.Model):
    _inherit = 'product.product'

    product_url = fields.Char(
        u'URL del producto', size=200,
        help=u'URL del curso original que se muestar en el sitio web')

    tot_hs_lecture = fields.Integer(
        u'Horas catedra',
        help=u"Cantidad de horas que tiene el curso en total.")

    hs_lecture = fields.Integer(
        u'Horas de clase',
        help=u"Duración de cada una de las clases.")

    agenda = fields.Text(
        u'Temario del curso',
        help=u"Descripción de los temas que abarca el curso, se formatea con markdown, "
             u"esta información se exporta al sitio web y se hace pública.")

    no_quotes = fields.Integer(
        u'Cantidad de cuotas', default=1,
        help=u'Cantidad de cuotas que tiene que pagar la aluman')

    default_registration_min = fields.Integer(
        u'Mínimo de alumnas en el curso', default=1,
        help=u"define la cantidad minima de alumnas para arrancar el curso. (Poner cero "
             u"para no tener en cuenta la regla)")

    default_registration_max = fields.Integer(
        u'Máximo de alumnas en el curso', default=9,
        help="Define la cantidad maxima de alumnas que puede tener el curso. (Poner cero "
             "para no tener en cuenta la regla)")

    default_email_registration = fields.Many2one(
        'email.template',
        u'Mail de inscripción',
        help=u"Selecciona el mail de inscripcion que se le enviara a la alumna")

    default_email_curso = fields.Many2one(
        'email.template',
        u'Mail de confirmacion',
        help=u"Selecciona el mail de confirmacion que se enviara a la alumna en el momento "
             u"de la confirmacion, esto es cuando paga o seña el curso")

    lecture_template_ids = fields.One2many(
        'curso.lecture_template', 'product_id', 'Clases',
        help=u"Contenido de cada clase, esto se usará de plantilla para copiar a cada "
             u"instancia de curso cuando esta se genere")

    curso_instances = fields.One2many(
        'curso.curso', 'product', 'Instancias',
        help=u'Instancias de este producto cuando es tipo (curso)')

    email_classes_ids = fields.One2many(
        'mail.template', 'product_id', 'templates',
        help=u"Definición de las plantillas de mail a enviar después de cada clase")

    @api.one
    @api.constrains('default_code','type')
    def _curso_unique_default_code(self):
        if self.type == 'curso':
            recordset = self.search([('default_code', '=', self.default_code)])
            if len(recordset) > 1:
                raise ValidationError('El curso {} {} ya está ingresado'.format(self.default_code,self.name))

    @api.one
    def button_generate_lecture_templates(self):
        no_clases = self.tot_hs_lecture / self.hs_lecture
        temp_obj = self.env['curso.lecture_template']
        temp_obj.create_template(self.id, no_clases)

    @api.multi
    def info_curso_html_data(self):
        data = {}
        data['name'] = self.name
        data['code'] = self.default_code
        data['description'] = self.description

        data['comercial_data'] = [
            u'Matricula bonificada.',
            u'No se cobra derecho de examen.',
            u'Materiales incluidos en el valor del curso.',
            u'Se entrega certificado contra examen aprobado.',
        ]
        data['curso_data'] = [
            u'Carga horaria {} horas.'.format(self.tot_hs_lecture),
            u'Duración 5 meses (20 semanas).',
            u'Modalidad 1 clase por semana.',
            u'Valor $1200 por mes.'
        ]

        data['instances'] = []
        for curso in self.curso_instances:
            print '-*------------------------------------------'
            print curso.date_begin
            print datetime.strptime(curso.date_begin,'%Y-%m-%d').strftime('%A')
            print '-*------------------------------------------'

            datetime.strptime(curso.date_begin,'%Y-%M-%d').strftime('%A')

            data['instances'].append(
                {'month': datetime.strptime(curso.date_begin,'%Y-%m-%d').strftime('%B'),
                 'day':datetime.strptime(curso.date_begin,'%Y-%m-%d').strftime('%-d'),
                 'name': curso.name,
                 'weekday': datetime.strptime(curso.date_begin,'%Y-%m-%d').strftime('%A'),
                 'schedule': curso.diary_ids[0].schedule.name,
                 'vacancy': u'Hay {} vacantes'.format(curso.register_avail),
             }
            )

        return data


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

