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
from datetime import datetime, date

from openerp import models, fields, api


class curso_curso(models.Model):
    _inherit = 'curso.curso'

    child = fields.Boolean(
        'Curso Hijo', readonly=True,
        states={'draft': [('readonly', False)]},
        help=u"Tildar si el curso es hijo, es decir debe estar insertado en un curso "
             u"mas grande")

    allow_overclass = fields.Boolean(
        'Permitir sobreclases', readonly=True,
        states={'draft': [('readonly', False)]},
        help=u"Tildar si cuando se generan clases se puede permitir que la clase "
             u"comparta el aula con otra en el mismo horario tener en cuenta que pasará "
             u"lo mismo con los feriados")

    instance = fields.Integer(
        'Instancia', readonly=True,
        states={'draft': [('readonly', False)]})

    register_max = fields.Integer(
        'Vacantes max', readonly=True,
        help=u"La cantidd máxima de vacantes del curso. Si la cantidad de "
             u"inscripciones es mayor, no se puede arrancar el curso. (poner 0 para "
             u"ignorar la regla)",
        states={'draft': [('readonly', False)]})

    register_min = fields.Integer(
        'Vacantes min', readonly=True,
        help=u"La cantidad mínima de inscripciones en el curso. Si no hay "
             u"suficientes inscripcones no se puede arrancar el curso. (poner 0 para "
             u"ignorar la regla)",
        states={'draft': [('readonly', False)]})

    date_begin = fields.Date(
        'Inicio', readonly=True,
        help=u"La fecha en la que inicia el curso, se puede dejar en blanco si no "
             u"está definida todavia pero se debe ingresar para confirmar el curso",
        states={'draft': [('readonly', False)]})

    reply_to = fields.Char(
        'Mail de respuesta', size=64, readonly=False,
        states={'done': [('readonly', True)]},
        help=u"La dirección de mail del que organiza los cursos, cuando el alumno "
             u"responde el mail que se le envia en automático responderá a esta dirección."
             u"si se deja en blanco la respuesta va a la dirección por defecto")

    note = fields.Text(
        'Description',
        states={'done': [('readonly', True)]})

    parent_curso_id = fields.Many2one(
        'curso.curso',
        'Curso padre donde se inserta este')

    first_lecture_id = fields.Many2one(
        'curso.lecture',
        'Clase inicial de este curso')

    user_id = fields.Many2one('res.users', string='Responsable',
                              default=lambda self: self.env.user,
                              readonly=False, states={'done': [('readonly', True)]})

    product = fields.Many2one(
        'product.product', 'Producto',
        required=True, readonly=True,
        domain="[('tot_hs_lecture','!=','0')]",
        states={'draft': [('readonly', False)]})

    email_registration_id = fields.Many2one(
        'email.template', 'Confirmación de inscripción',
        help=u'Plantilla de mail que se enviará cada vez que un alumno de este curso '
             u'pase al estado señado.')

    email_confirmation_id = fields.Many2one(
        'email.template', 'Confirmación curso',
        help=u"Si definis una plantilla de mail, cada participante recibirá este "
             u"mail anunciando la confirmación del curso.")

    main_speaker_id = fields.Many2one(
        'res.partner', 'Profesora', readonly=False,
        states={'done': [('readonly', True)]},
        help=u"La profesora que va a dar el curso.")

    company_id = fields.Many2one(
        'res.company', string='Company', change_default=True,
        default=lambda self: self.env['res.company']._company_default_get('curso.curso'),
        required=False, readonly=False, states={'done': [('readonly', True)]})

    registration_ids = fields.One2many(
        'curso.registration', 'curso_id', 'Inscripciones',
        states={'done': [('readonly', True)],
                'cancel': [('readonly', True)]})

    lecture_ids = fields.One2many(
        'curso.lecture', 'curso_id', 'Clases')

    diary_ids = fields.One2many(
        'curso.diary', 'curso_id', 'Agenda', readonly=True,
        states={'draft': [('readonly', False)]})

    email_classes_ids = fields.One2many(
        'mail.template', 'curso_id', 'templates',
        help=u"Definición de las plantillas de mail a enviar después de cada clase")

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirm', 'Cursando'),
        ('done', 'Cumplido'),
        ('cancel', 'Cancelado')
    ],
        'Estado', readonly=True, required=True,
        help=u"Cuando se crea el curso el estado es 'Borrador'. Si se confirma el "
             u"curso el estado es 'Cursando'. Si el curso termina el estado "
             u"es 'Cumplido'. Si el curso es cancelado el estado pasa a 'Cancelado'.",
        default='draft')

    tot_hs_lecture = fields.Integer(
        related='product.tot_hs_lecture', readonly=True,
        string='Tot Hs')

    list_price = fields.Float(
        related='product.list_price', readonly=True,
        string='Cuota')

    hs_lecture = fields.Integer(
        related='product.hs_lecture', readonly=True,
        string='Hs')

    default_code = fields.Char(
        related='product.default_code', readonly=True,
        string=u'Código')

    no_quotes = fields.Integer(
        related='product.no_quotes', readonly=True,
        string='#cuotas')

    country_id = fields.Many2one('res.country', string='Country',
                                 store=True, compute='_compute_country')

    register_attended = fields.Integer(
        compute='_get_register_',
        string='Egresadas',
        help=u"Cantidad de alumnas que termino el curso con exito.")

    register_current = fields.Integer(
        compute='_get_register_',
        string='Alumnas',
        help=u"La cantidad de alumnas que confirmaron pagando (al menos una seña)")

    register_avail = fields.Integer(
        compute='_get_register_',
        string='Vacantes')

    register_prospect = fields.Integer(
        compute='_get_register_',
        string='Interesadas',
        help=u"La cantidad de alumnas interesadas que todavía no concretaron")

    is_subscribed = fields.Boolean(
        compute='_subscribe_fnc_',
        string='Subscribed')

    next = fields.Boolean(
        compute='_get_next_',
        string='Curso por venir')

    classes_per_week = fields.Integer(
        compute='_get_classes_per_week_',
        string='Clases por semana',
        help=u"La cantidad de clases por semana")

    curso_instance = fields.Char(
        compute='_get_instance_', string='Instancia del curso')

    name = fields.Char(
        compute='_get_name_',
        store=True,
        string='Nombre del curso')

    no_lectures = fields.Char(
        compute='_get_no_lectures_', string='Clases',
        help=u"La cantidad de clases que tiene el curso")

    address_id = fields.Many2one('res.partner', string='Location',
                                 default=lambda self: self.env.user.company_id.partner_id,
                                 readonly=False, states={'done': [('readonly', True)]})

    @api.one
    @api.depends('registration_ids.user_id', 'registration_ids.state')
    def _subscribe_fnc_(self):
        """ Determine whether the current user is already subscribed to any event in `self` """
        user = self.env.user
        self.is_subscribed = any(
            reg.user_id == user and reg.state in ('open', 'done')
            for reg in self.registration_ids
        )

    @api.one
    @api.depends('register_max', 'registration_ids.state', 'registration_ids.nb_register')
    def _get_register_(self):
        reg_open = reg_done = reg_draft = 0

        for registration in self.registration_ids:
            if registration.state == 'confirm':
                reg_open += registration.nb_register
            elif registration.state == 'done':
                reg_done += registration.nb_register
            elif registration.state == 'draft':
                reg_draft += registration.nb_register

        self.register_current = reg_open
        self.register_attended = reg_done
        self.register_prospect = reg_draft
        # the number of ticket is unlimited if the curso.register_max field is not set.
        # In that cas we arbitrary set it to 9999, it is used in the
        # kanban view to special case the display of the 'subscribe' button
        self.register_avail = self.register_max - reg_open if self.register_max != 0 else 9999

    @api.one
    @api.depends('date_begin')
    def _get_next_(self):
        # si no tiene fecha o está en el futuro es true
        next = True
        if self.date_begin:
            if self.date_begin < str(date.today()):
                self.next = False

    @api.one
    def _get_classes_per_week_(self):
        """ Calcula la cantidad de clases por semana basado en el diary
        """
        diary_obj = self.env['curso.diary']
        ids = diary_obj.search([('curso_id', '=', self.id)])
        self.classes_per_week = len(ids)

    @api.one
    @api.depends('default_code', 'instance')
    def _get_instance_(self):
        self.curso_instance = self.get_formatted_instance(self.id)

    @api.one
    @api.depends('date_begin', 'curso_instance', 'product.name')
    def _get_name_(self):
        try:
            init = datetime.strptime(self.date_begin, "%Y-%m-%d")
        except:
            weekday = day_n = month_n = year_n = '?'
        else:
            weekday = init.strftime("%a").capitalize()
            day_n = init.strftime('%d')
            month_n = init.strftime('%m')
            year_n = init.strftime('%y')
        diary_obj = self.env['curso.diary']
        hhs = mms = hhe = mme = 0
        for diary_line in diary_obj.search([('curso_id', '=', self.id)]):
            ss = diary_line.schedule.start_time
            ee = diary_line.schedule.end_time
            mms = ss - int(ss)
            hhs = int(ss - mms)
            mms = int(mms * 60)
            mme = ee - int(ee)
            hhe = int(ee - mme)
            mme = int(mme * 60)
            break

        # https://docs.python.org/2/library/datetime.html#datetime-objects
        self.name = u'[{}] {} {}/{}/{} ({:0>2d}:{:0>2d} {:0>2d}:{:0>2d}) - {}'.format(
            self.curso_instance,
            # Codigo de producto, Nro de instancia
            unicode(weekday.capitalize(), 'utf-8'),  # dia de la semana en letras
            day_n, month_n, year_n,  # dia , mes, anio en numeros
            hhs, mms, hhe, mme,  # hora de inicio hora de fin
            self.product.name)  # nombre del producto

    @api.one
    @api.depends('tot_hs_lecture', 'hs_lecture')
    def _get_no_lectures_(self):
        try:
            self.no_lectures = int(self.tot_hs_lecture / self.hs_lecture)
            if self.tot_hs_lecture % self.hs_lecture != 0:
                raise
        except:
            self.no_lectures = 'Error!'

    @api.one
    @api.depends('address_id')
    def _compute_country(self):
        self.country_id = self.address_id.country_id

    @api.one
    def get_calendar(self):
        # extrae los datos de calendario de la data, ahi estań todas las instancias
        # se trae la linea que coincide con la instancia del curso. si el curso tiene
        # mas de una linea esto no va a funcionar ie distintos horarios en una semana.
        def extract(data, curso_instance):
            res = []
            for dic in data:
                if dic.get('instancia', 'nada') == curso_instance:
                    res.append(dic)
            return res

        data = self.product._get_wordpress_data(self.default_code)
        calendar = extract(data['grid'], self.curso_instance)
        avail = data['vacantes']

        res = []
        for dict in calendar:
            new = {}
            if dict.get('horario', '&nbsp;') != '&nbsp;':
                new['schedule'] = dict.get('horario')

            if dict.get('instancia', '&nbsp;') != '&nbsp;':
                new['code'] = dict.get('instancia')

            if dict.get('dias', '&nbsp;') != '&nbsp;':
                new['days'] = dict.get('dias')

            if dict.get('inicio', '&nbsp;') != '&nbsp;':
                new['begin'] = dict.get('inicio')
            if len(new) > 0:
                new['avail'] = avail
            res.append(new)

        return res


"""
{'description': u'<blockquote>\n<p>Regalate o regal\xe1 un curso de automaquillaje. </p>\n</blockquote>\n<p>Ven\xed a disfrutar del d\xeda y aprend\xe9 a maquillarte!\n Animate a pasar una tarde distinta aprendiendo tips y consejos para verte m\xe1s linda, maquillada como una profesional</p>',
 'temario': u'<ul>\n<li>Preparaci\xf3n y cuidados de la piel (t\xe9cnicas y productos de higiene)</li>\n<li>Mofolog\xeda del rostro correcciones y bases</li>\n<li>Belleza: Rubor y ojos (sombras y delineados)</li>\n<li>Labios y paleta de colores (maquillaje d\xeda / noche)</li>\n</ul>',
 'grid':
     [
         {'horario': u'16:00 - 18:00 (2hs)', 'instancia': 'G01/09', 'dias': u'Mi\xe9rcoles', 'inicio': '01/06/2016'},
         {'horario': '&nbsp;', 'instancia': '&nbsp;', 'dias': '&nbsp;', 'inicio': '&nbsp;'},
         {'horario': u'11:30 - 13:30 (2hs)', 'instancia': 'G01/12', 'dias': u'S\xe1bado', 'inicio': '25/06/2016'},
         {'horario': '&nbsp;', 'instancia': '&nbsp;', 'dias': '&nbsp;', 'inicio': '&nbsp;'},
         {'horario': u'09:30 - 11:30 (2hs)', 'instancia': 'G01/16', 'dias': u'S\xe1bado', 'inicio': '25/06/2016'},
         {'horario': '&nbsp;', 'instancia': '&nbsp;', 'dias': '&nbsp;', 'inicio': '&nbsp;'},
         {'horario': u'18:30 - 20:30 (2hs)', 'instancia': 'G01/15', 'dias': u'Lunes', 'inicio': '27/06/2016'},
         {'horario': '&nbsp;', 'instancia': '&nbsp;', 'dias': '&nbsp;', 'inicio': '&nbsp;'},
         {'horario': u'15:00 - 17:00 (2hs)', 'instancia': 'G01/14', 'dias': u'Martes', 'inicio': '28/06/2016'},
         {'horario': '&nbsp;', 'instancia': '&nbsp;', 'dias': '&nbsp;', 'inicio': '&nbsp;'},
         {'horario': u'16:00 - 18:00 (2hs)', 'instancia': 'G01/17', 'dias': u'Viernes', 'inicio': '15/07/2016'},
         {'horario': '&nbsp;', 'instancia': '&nbsp;', 'dias': '&nbsp;', 'inicio': '&nbsp;'},
         {'horario': u'18:30 - 20:30 (2hs)', 'instancia': 'G01/18', 'dias': u'Viernes', 'inicio': '22/07/2016'},
         {'horario': '&nbsp;', 'instancia': '&nbsp;', 'dias': '&nbsp;', 'inicio': '&nbsp;'},
         {'horario': u'09:30 - 11:30 (2hs)', 'instancia': 'G01/19', 'dias': u'S\xe1bado', 'inicio': '23/07/2016'},
         {'horario': '&nbsp;', 'instancia': '&nbsp;', 'dias': '&nbsp;', 'inicio': '&nbsp;'},
         {'horario': u'18:30 - 20:30 (2hs)', 'instancia': 'G01/20', 'dias': u'Lunes', 'inicio': '25/07/2016'},
         {'horario': '&nbsp;', 'instancia': '&nbsp;', 'dias': '&nbsp;', 'inicio': '&nbsp;'},
         {'horario': u'11:30 - 13:30 (2hs)', 'instancia': 'G01/21', 'dias': u'S\xe1bado', 'inicio': '30/07/2016'},
         {'horario': '&nbsp;', 'instancia': '&nbsp;', 'dias': '&nbsp;', 'inicio': '&nbsp;'},
         {'horario': u'16:00 - 18:00 (2hs)', 'instancia': 'G01/22', 'dias': u'Lunes', 'inicio': '01/08/2016'},
         {'horario': '&nbsp;', 'instancia': '&nbsp;', 'dias': '&nbsp;', 'inicio': '&nbsp;'},
         {'horario': u'18:30 - 20:30 (2hs)', 'instancia': 'G01/23', 'dias': u'Mi\xe9rcoles', 'inicio': '03/08/2016'},
         {'horario': '&nbsp;', 'instancia': '&nbsp;', 'dias': '&nbsp;', 'inicio': '&nbsp;'},
         {'horario': u'14:00 - 16:00 (2hs)', 'instancia': 'G01/24', 'dias': u'Jueves', 'inicio': '04/08/2016'},
         {'horario': '&nbsp;', 'instancia': '&nbsp;', 'dias': '&nbsp;', 'inicio': '&nbsp;'},
         {'horario': u'16:00 - 18:00 (2hs)', 'instancia': 'G01/25', 'dias': u'Martes', 'inicio': '09/08/2016'},
         {'horario': '&nbsp;', 'instancia': '&nbsp;', 'dias': '&nbsp;', 'inicio': '&nbsp;'},
         {'horario': u'14:00 - 16:00 (2hs)', 'instancia': 'G01/26', 'dias': u'Viernes', 'inicio': '19/08/2016'},
         {'horario': '&nbsp;', 'instancia': '&nbsp;', 'dias': '&nbsp;', 'inicio': '&nbsp;'},
         {'horario': u'18:30 - 20:30 (2hs)', 'instancia': 'G01/27', 'dias': u'Viernes', 'inicio': '26/08/2016'},
         {'horario': '&nbsp;', 'instancia': '&nbsp;', 'dias': '&nbsp;', 'inicio': '&nbsp;'}
     ],
     'titulo': u'Curso de Automaquillaje',
     'matricula': 'Bonificada',
     'modalidad': u'Modalidad: una clase de 2 horas por semana',
     'vacantes': 3,
     'valor': '299.0',
     'duracion': u'Duraci\xf3n 4 semanas, (8 hs)',
     'codigo': u'G01',
     'cuotas': '1'
 }
"""
