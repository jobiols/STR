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
from openerp.exceptions import ValidationError

from . import html_filter


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
        comodel_name='mails.to.send',
        inverse_name='product_id',
        string='templates',
        help=u"Definición de las plantillas de mail a enviar después de cada clase",
    )

    public_price = fields.Float(
        u'Precio púb',
        compute='_compute_prices'
    )

    pro_price = fields.Float(
        u'Precio pro',
        compute='_compute_prices'
    )

    mercadopago_button = fields.Char(
        u'Boton de mercadopago precio normal'
    )

    mercadopago_button_discount = fields.Char(
        u'Boton de mercadopago con descuento'
    )

    mercadopago_discount = fields.Float(
        u'Descuento mercadopago',
        digits=(2,8)
    )

    woo_id = fields.Char(
        help=u'Identifica el producto en woo'
    )

    woo_categ = fields.Many2one(
        'curso.woo.categ',
        'Categoría de producto',
        help=u'Categoría de producto'
    )

    description_short_wc = fields.Char(
        compute="_compute_short_wc",
        store="True"
    )

    comercial_data = fields.Char(
        'datos comerciales',
        help=u"Información que aparece en el sitio y en los mails",
    )

    nube_id = fields.Integer(
        help=u'Identifica el producto en tienda nube'
    )

    @api.one
    @api.depends('description')
    def _compute_short_wc(self):
        if self.description:
            ix = self.description.find('<mas>')
            if ix == -1:
                # no existe el simbolo <mas>
                if len(self.description) < 400:
                    self.description_short_wc = \
                        u'OK Total {} caracteres.'.format(len(self.description))
                else:
                    self.description_short_wc = \
                        u'Debe incluir el simbolo <mas> para reducir la cantidad de caracteres!!'
            else:
                # existe el simbolo <mas>
                if ix < 400:
                    self.description_short_wc = \
                        u'OK Total {} caracteres antes del símbolo <mas>'.format(ix)
                else:
                    self.description_short_wc = \
                        u'Total {} DEMASIADOS CARACTERES ANTES DE <mas> max 400'.format(ix)

    @api.one
    @api.depends('lst_price', 'standard_price')
    def _compute_prices(self):
        # TODO poner ensto en una configuracion
        public_pricelist_id = 1
        pro_pricelist_id = 3

        # calcular el precios basado en la lista de precios
        self.public_price = self.pool.get('product.pricelist').price_get(
            self.env.cr, self.env.uid, [public_pricelist_id], self.id, 1.0,
            context=None)[public_pricelist_id]

        self.pro_price = self.pool.get('product.pricelist').price_get(
            self.env.cr, self.env.uid, [pro_pricelist_id], self.id, 1.0,
            context=None)[pro_pricelist_id]

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
        """ informacion para armar el html.
            El debug es para correr los tests!!
            resulta que debe traer cursos futuros, y las fechas de las cosas
            en los tests estan harcodeadas y fué mas facil aunque dirty
            harcodearlas que hacerlas dinamicas.
        """
        data = {}
        data['name'] = self.name
        data['code'] = self.default_code
        data['description'] = markdown.markdown(self.description)
        data['no_lectures'] = self.tot_hs_lecture / self.hs_lecture
        data['hs_lecture'] = self.hs_lecture
        clases = int(self.tot_hs_lecture / self.hs_lecture)
        horas = self.hs_lecture
        if clases == 1:
            str_ = 'Es {} clase de {} horas'
            clases = 'una'
        else:
            str_ = 'Son {} clases de {} horas c/u'
        data['mode'] = str_.format(clases, horas)
        data['product_url'] = self.product_url
        data['temario'] = markdown.markdown(self.agenda)
        data['comercial_data'] = (self.comercial_data or '').split(',')
        dur_weeks = self.tot_hs_lecture / self.hs_lecture
        data['curso_data'] = [
            u'Carga horaria {} horas.'.format(self.tot_hs_lecture),
            u'Duración {} semanas.'.format(dur_weeks)
        ]
        data['curso_price'] = self.list_price
        data['curso_price_per'] = '' if dur_weeks <= 4 else 'por mes'
        if self.mercadopago_button:
            data['mercadopago_button'] = self.mercadopago_button
        if self.mercadopago_button_discount:
            data['mercadopago_button_discount'] = self.mercadopago_button_discount
        if self.mercadopago_discount:
            data['mercadopago_discount'] = self.mercadopago_discount

        def calc_vacancy(vac):
            ret = u'<p style="color:{};">{}</p>'
            if vac <= 0:
                return ret.format('red', 'No hay vacantes!!')
            if vac <= 2:
                return ret.format('orange', 'Pocas vacantes!')
            if vac > 2:
                return ret.format('green', 'Vacantes disponibles')

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
                      ('date_begin', '!=', False),
                      ('state', '!=', 'cancel')]

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
    def build_html_page(self):
        data = self.info_curso_html_data()
        html = html_filter.html_filter()
        ret = html.default_header(data)
        ret += html.temario_curso(data)
        ret += html.inicios_curso(data)
        ret += html.entrega_certificado(data)
        ret += html.info_curso(data, col=1)
        return ret

    @api.multi
    def button_generate_doc(self):
        """ Generate html data for curso
        """
        html = html_filter.html_filter()
        for prod in self:
            new_page = {
                'name': prod.name,
                'content': self.build_html_page(),
            }
            # Borrar el documento si es que existe
            docs = self.env['document.page']
            records = docs.search([('name', '=', prod.name)])
            records.unlink()
            # Crear el documento
            docs.create(new_page)

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
