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
from openerp import models, fields


class product_template(models.Model):
    _inherit = 'product.template'
    type = fields.Selection(selection_add=[('curso', 'Curso')])


class product_product(models.Model):
    _inherit = 'product.product'

    product_url = fields.Char(
        'URL del producto', size=200)
    tot_hs_lecture = fields.Integer(
        'Horas catedra',
        help="Cantidad de horas que tiene el curso en total.")
    hs_lecture = fields.Integer(
        'Horas de clase',
        help="Duración de cada una de las clases.")

    agenda = fields.Text(
        'Tema')

    no_quotes = fields.Integer(
        'Cantidad de cuotas',
        default = 1)

    default_reply_to = fields.Char(
        'Respuesta por defecto', size=64,
        help="El mail del organizador, que se pondra en el campo de respuesta de todos "
             "los mails enviados automaticamente en inscripciones y confirmaciones de cursos.")

    default_registration_min = fields.Integer(
        'Minimo de alumnas en el curso',
        default = 1,
        help="define la cantidad minima de alumnas para arrancar el curso. (Pone cero para "
             "no tener en cuenta la regla)")

    default_registration_max = fields.Integer(
        'Maximo de alumnas en el curso',
        default = 9,
        help="Define la cantidad maxima de alumnas que puede tener el curso. (Pone cero para "
             "no tener en cuenta la regla)")

    default_email_registration = fields.Many2one(
        'email.template',
        'Mail de inscripcion',
        help="Selecciona el mail de inscripcion que se le enviara a la alumna")

    default_email_curso = fields.Many2one(
        'email.template',
        'Mail de confirmacion',
        help="Selecciona el mail de confirmacion que se enviara a la alumna en el momento "
             "de la confirmacion")

    lecture_template_ids = fields.One2many(
        'curso.lecture_template', 'product_id', 'Clases')

    curso_instances = fields.One2many(
        'curso.curso', 'product', 'Instancias'
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
