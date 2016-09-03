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

import markdown

from openerp import models, fields, api
from openerp.exceptions import ValidationError, Warning


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
        comodel_name='mail.template',
        inverse_name='product_id',
        string='templates',
        help=u"Definición de las plantillas de mail a enviar después de cada clase",
    )

    @api.one
    @api.constrains('default_code', 'type')
    def _curso_unique_default_code(self):
        if self.type == 'curso':
            recordset = self.search([('default_code', '=', self.default_code)])
            if len(recordset) > 1:
                raise ValidationError(
                    'El curso {} {} ya está ingresado'.format(self.default_code,
                                                              self.name))

    @api.one
    def button_generate_lecture_templates(self):
        no_clases = self.tot_hs_lecture / self.hs_lecture
        temp_obj = self.env['curso.lecture_template']
        temp_obj.create_template(self.id, no_clases)

    @api.multi
    def info_curso_html_data(self, debug=False):
        def get_quote_price(dur_weeks, price):
            if dur_weeks <= 4:
                return u'<strong>Valor ${}</strong>'.format(price)
            else:
                return u'<strong>Valor ${} por mes</strong>'.format(price)

        data = {}
        data['name'] = self.name
        data['code'] = self.default_code
        data['description'] = self.description
        data['no_lectures'] = self.tot_hs_lecture / self.hs_lecture
        data['hs_lecture'] = self.hs_lecture
        data['product_url'] = self.product_url

        data['comercial_data'] = [
            u'Matricula bonificada.',
            u'No se cobra derecho de examen.',
            u'Materiales incluidos en el valor del curso.',
            u'Se entrega certificado digital.',
        ]
        dur_weeks = self.tot_hs_lecture / self.hs_lecture
        data['curso_data'] = [
            u'Carga horaria {} horas.'.format(self.tot_hs_lecture),
            u'Duración {} semanas.'.format(dur_weeks),
            get_quote_price(dur_weeks, self.list_price)
        ]

        def calc_vacancy(vac):
            ret = u'<p style="color:{};">{}</p>'
            if vac <= 0:
                return ret.format('red', 'No hay vacantes!!')
            if vac <= 2:
                return ret.format('orange', 'Pocas vacantes!')
            if vac > 2:
                return ret.format('green', 'Hay vacantes')

        def get_schedule(curso):
            try:
                ret = curso.diary_ids[0].schedule.name
            except:
                ret = 'Horario no definido'
            return ret

        data['instances'] = []
        if debug:
            domain = [('product', '=', self.id),
                      ('date_begin', '!=', False)]
        else:
            domain = [('next', '=', True),
                      ('product', '=', self.id),
                      ('date_begin', '!=', False)]

        for curso in self.curso_instances.search(domain):
            # trae cursos en el futuro, con fecha
            # TODO quitar estos chequeos de fecha
            try:
                dt = datetime.strptime(curso.date_begin, '%Y-%m-%d')
            except:
                dt = False

            mon = dt.strftime('%B') if dt else '?'
            day = dt.strftime('%-d') if dt else '?'
            wee = dt.strftime('%A').decode('utf-8', 'ignore') if dt else '?'
            year = dt.strftime('%Y')
            data['instances'].append(
                {'month': mon.capitalize() + ' ' + year,
                 'day': day,
                 'name': curso.name,
                 'weekday': wee.capitalize(),
                 'schedule': get_schedule(curso),
                 'vacancy': calc_vacancy(curso.register_avail),
                 'curso_instance': curso.curso_instance
                 })

        return data

    @api.multi
    def button_generate_doc(self):
        """ Generate html data for curso """
        html = self.env['html_filter']
        for prod in self:
            data = self._get_wordpress_data(prod.default_code)
            if not data:
                raise Warning(
                    'Error!',
                    'No hay instancias de cursos para este producto!')

            new_page = {
                'name': prod.name,
                'content': html.generate_html([data]),
            }
            # Borrar el documento si es que existe
            docs = self.env['document.page']
            records = docs.search([('name', '=', prod.name)])
            records.unlink()
            # Crear el documento
            docs.create(new_page)

    @api.multi
    def _get_wordpress_data(self, default_code):
        """ Genera el los datos para pegar html, trae todas las instancias de cursos
            basadas en este producto.
        """
        data = {}
        for prod in self:
            curso_obj = self.env['curso.curso']
            # traer cursos por default code, con fecha de inicio y en estado
            # draft o confirm

            cursos = curso_obj.search([
                ('default_code', '=', prod.default_code),
                ('date_begin', '<>', False),
                '|',
                ('state', '=', 'draft'),
                ('state', '=', 'confirm')
            ])
            grid = []
            data = False
            for curso in cursos:
                formatted_diary = self._get_formatted_diary(curso.id)
                for idx, fdline in enumerate(formatted_diary):
                    if idx == 0:
                        grid.append(
                            {'inicio': datetime.strptime(curso.date_begin,
                                                         '%Y-%m-%d').strftime('%d/%m/%Y'),
                             'instancia': curso.get_formatted_instance(curso.id),
                             'dias': fdline['dias'],
                             'horario': fdline['horario'],
                             })
                    else:
                        grid.append(
                            {'inicio': '',
                             'instancia': '',
                             'dias': fdline['dias'],
                             'horario': fdline['horario'],
                             })
                grid.append(
                    {'inicio': '&nbsp;',
                     'instancia': '&nbsp;',
                     'dias': '&nbsp;',
                     'horario': '&nbsp;',
                     })
                try:
                    weeks = \
                        (prod.tot_hs_lecture / prod.hs_lecture) / curso.classes_per_week
                except:
                    weeks = "error!"

                # si está vacio trae False y da una excepcion en mark_down
                if not prod.agenda:
                    prod.agenda = ''
                if not prod.description:
                    prod.description = ''

                if weeks > 1:
                    duracion = u'Duración %s semanas, (%s hs)' % (
                        weeks, prod.tot_hs_lecture)
                    if curso.classes_per_week > 1:
                        modalidad = u'Modalidad: %s clases de %s hs por semana' % (
                            curso.classes_per_week, prod.hs_lecture)
                    else:
                        modalidad = u'Modalidad: una clase de %s horas por semana' % (
                            prod.hs_lecture)
                else:
                    duracion = ''
                    if curso.classes_per_week > 1:
                        modalidad = u'Modalidad: %s clases de %s hs' % (
                            curso.classes_per_week, prod.hs_lecture)
                    else:
                        modalidad = u'Modalidad: una clase de %s horas' % (
                            prod.hs_lecture)

                data = {
                    'titulo': prod.name,
                    'codigo': prod.default_code,
                    'description': markdown.markdown(prod.description),
                    'duracion': duracion,
                    'modalidad': modalidad,
                    'grid': grid,
                    'temario': markdown.markdown(prod.agenda),
                    'matricula': 'Bonificada',
                    'cuotas': str(prod.no_quotes),
                    'valor': str(prod.list_price),
                    'vacantes': 3
                }

                if False:
                    print '-------------------------------------------------'
                    print data
                    print '-------------------------------------------------'
                    print 'titulo           ', data['titulo']
                    print 'codigo           ', data['codigo']
                    print 'description      ', data['description']
                    print 'duracion         ', data['duracion']
                    print 'modalidad        ', data['modalidad']
                    for dd in data['grid']:
                        print 'grid-data    ', dd
                    print 'temario          ', data['temario']
                    print 'matricula        ', data['matricula']
                    print 'cuotas           ', data['cuotas']
                    print 'valor            ', data['valor']
                    print '-------------------------------------------------'

        return data

    def find_schedule(self, list, data):
        for l in list:
            if l['horario'] == data:
                return l
        return False

    def _get_formatted_diary(self, curso_id):
        """
        Devuelve una lista con las lineas del diario agrupadas por horario y ordenadas por dia.
        Si un horario se repite en varios dias pone coma entres los dias.
        """
        formatted_diary = []
        diary = []

        # bajar el diary completo a la lista diary
        diary_obj = self.env['curso.diary']
        for dl in diary_obj.search([('curso_id', '=', curso_id)]):
            diary.append({
                'weekday': dl.weekday,
                'weekday_name': dl.weekday_name,
                'schedule': dl.schedule.name,
                'seq': dl.seq
            })

        # recorrer diary agrupando por schedule
        for diary_line in diary:
            # obtengo una referencia a la linea
            fd_line = self.find_schedule(formatted_diary, diary_line['schedule'])
            if fd_line:
                # si existe el horario le agrego el día a la lista de dias
                fd_line['list_dias'].append(diary_line['weekday_name'])
            else:
                # no existe el horario agrego la linea
                formatted_diary.append(
                    {'list_dias': [diary_line['weekday_name']],
                     'horario': diary_line['schedule']
                     })

        # hacer la lista de dias formateada
        for fdl in formatted_diary:
            fdl['dias'] = ', '.join(fdl['list_dias'])

        return formatted_diary

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
