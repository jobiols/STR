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
import operator

from openerp.exceptions import ValidationError
from openerp import models, fields, api
from openerp.exceptions import Warning


class curso_curso(models.Model):
    _inherit = 'curso.curso'

    child = fields.Boolean(
        u'Curso Hijo', readonly=True,
        states={'draft': [('readonly', False)]},
        help=u"Tildar si el curso es hijo, es decir debe estar insertado en un curso "
             u"mas grande")

    allow_overclass = fields.Boolean(
        u'Permitir sobreclases', readonly=True,
        states={'draft': [('readonly', False)]},
        help=u"Tildar si cuando se generan clases se puede permitir que la clase "
             u"comparta el aula con otra en el mismo horario tener en cuenta que pasará "
             u"lo mismo con los feriados")

    instance = fields.Integer(
        u'Instancia', readonly=True,
        states={'draft': [('readonly', False)]})

    register_max = fields.Integer(
        u'Vacantes max', readonly=True,
        help=u"La cantidd máxima de vacantes del curso. Si la cantidad de "
             u"inscripciones es mayor, no se puede arrancar el curso. (dejar en blanco para "
             u"ignorar la regla)",
        states={'draft': [('readonly', False)]})

    register_min = fields.Integer(
        u'Vacantes min', readonly=True,
        help=u"La cantidad mínima de inscripciones en el curso. Si no hay "
             u"suficientes inscripcones no se puede arrancar el curso. (poner 0 para "
             u"ignorar la regla)",
        states={'draft': [('readonly', False)]})

    date_begin = fields.Date(
        u'Inicio', readonly=True,
        help=u"La fecha en la que inicia el curso, se puede dejar en blanco si no "
             u"está definida todavia pero se debe ingresar para confirmar el curso",
        states={'draft': [('readonly', False)]})

    reply_to = fields.Char(
        u'Mail de respuesta', size=64,
        states={'done': [('readonly', True)]},
        help=u"La dirección de mail del que organiza los cursos, cuando el alumno "
             u"responde el mail que se le envia en automático responderá a esta dirección."
             u"si se deja en blanco la respuesta va a la dirección por defecto")

    note = fields.Text(
        u'Descripción',
        states={'done': [('readonly', True)]})

    parent_curso_id = fields.Many2one(
        'curso.curso',
        u'Curso padre donde se inserta este')

    first_lecture_id = fields.Many2one(
        'curso.lecture',
        u'Clase inicial de este curso')

    user_id = fields.Many2one(
        'res.users', string=u'Responsable',
        default=lambda self: self.env.user,
        readonly=False, states={'done': [('readonly', True)]})

    product = fields.Many2one(
        'product.product', u'Producto',
        required=True, readonly=True,
        domain="[('tot_hs_lecture','!=','0')]",
        states={'draft': [('readonly', False)]},
        help=u'Producto de donde este curso fue generado')

    email_registration_id = fields.Many2one(
        'email.template', u'Confirmación de inscripción',
        help=u'Plantilla de mail que se enviará cada vez que un alumno de este curso '
             u'pase al estado señado.')

    email_confirmation_id = fields.Many2one(
        'email.template', u'Confirmación curso',
        help=u"Si definis una plantilla de mail, cada participante recibirá este "
             u"mail anunciando la confirmación del curso.")

    main_speaker_id = fields.Many2one(
        'res.partner', u'Profesora', required=True,
        states={'done': [('readonly', True)]},
        help=u"La profesora que va a dar el curso.")

    secondary_speaker_id = fields.Many2one(
        'res.partner', u'Asistente',
        states={'done': [('readonly', True)]},
        help=u"La asistente del curso.")

    company_id = fields.Many2one(
        'res.company', string='Company', change_default=True,
        default=lambda self: self.env['res.company']._company_default_get('curso.curso'),
        required=False, readonly=False, states={'done': [('readonly', True)]})

    registration_ids = fields.One2many(
        'curso.registration', 'curso_id', u'Inscripciones',
        states={'done': [('readonly', True)],
                'cancel': [('readonly', True)]})

    lecture_ids = fields.One2many(
        'curso.lecture', 'curso_id', u'Clases',
        help='Las clases que componen este curso')

    diary_ids = fields.One2many(
        'curso.diary', 'curso_id', u'Agenda', readonly=True,
        states={'draft': [('readonly', False)]},
        help='Define los dias y horarios en los que se da el curso')

    state = fields.Selection([
        ('draft', 'Borrador'),  # estado inicial
        ('confirm', 'Confirmado'),  # se publica
        ('in_progress', 'Cursando'),  # está activo, verifica fechas inicio - fin
        ('done', 'Cumplido'),  # está cumpllido verifica fechas fin
        ('cancel', 'Cancelado')  # está cancelado no se publica
    ],
        'Estado', readonly=True, required=True,
        default='draft',
        help=u"Borrador:   Está recién creado\n"
             u"Confirmado: Se publica en el sitio\n"
             u"Cursando:   Está activo, se verifica que con las fechas de primera y ultima clase\n"
             u"Cumplido:   Terminó la fecha es posterior a la de la ultima clase\n'."
             u"Cancelado:  Desaparece de la publicacion'.")

    tot_hs_lecture = fields.Integer(
        related='product.tot_hs_lecture', readonly=True,
        string=u'Tot Hs',
        help=u'Cantidad total de horas cátedra del curso')

    list_price = fields.Float(
        related='product.list_price', readonly=True,
        string='Cuota',
        help=u'Es el valor de la cuota, o el total si es solo un pago.')

    hs_lecture = fields.Integer(
        related='product.hs_lecture', readonly=True,
        string=u'Hs')

    default_code = fields.Char(
        related='product.default_code', readonly=True,
        string=u'Código',
        help=u'Código por defecto del producto')

    no_quotes = fields.Integer(
        related='product.no_quotes', readonly=True,
        string='#cuotas',
        help=u'Cantidad de cuotas para pagar el curso')

    country_id = fields.Many2one(
        'res.country', string='Country',
        store=True, compute='_compute_country')

    register_attended = fields.Integer(
        compute='_get_register',
        string='Egresadas',
        help=u"Cantidad de alumnas que termino el curso con exito.")

    register_current = fields.Integer(
        compute='_get_register',
        string='Confirmadas',
        help=u"La cantidad de alumnas que confirmaron pagando (al menos una seña)")

    register_avail = fields.Integer(
        compute='_get_register',
        string='Vacantes',
        help=u"La cantidad de vacantes que le queda al curso")

    register_prospect = fields.Integer(
        compute='_get_register',
        string='Interesadas',
        help=u"La cantidad de alumnas interesadas que todavía no concretaron")

    register_cancel = fields.Integer(
        compute='_get_register',
        string='Canceladas',
        help=u"La cantidad de alumnas que cancelaron el curso")

    is_subscribed = fields.Boolean(
        compute='_subscribe_fnc_',
        string='Subscribed')

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

    address_id = fields.Many2one(
        'res.partner', string='Location',
        default=lambda self: self.env.user.company_id.partner_id,
        readonly=False, states={'done': [('readonly', True)]})

    @api.constrains('date_begin', 'diary_ids')
    def _check_first_date(self):
        """ Verifica que la fecha de inicio sea el primer dia del diary
            Si no tiene fecha de inicio no chequea nada
        """
        try:
            # fecha de inicio
            dt = datetime.strptime(self.date_begin, '%Y-%m-%d')
            date_begin = dt.strftime('%d/%m/%Y')            # fecha
            date_begin_day = dt.strftime('%A').decode('utf-8', 'ignore').capitalize()  # nombre del dia
            wd_date_no = dt.strftime('%w')                  # numero de dia de la semana

            # diario
            dry = self.diary_ids[0]
            weekday = dry.weekday_name  # nombre del dia
            wd_diary_no = dry.weekday  # código del dia
        except:
            wd_date_no = wd_diary_no = 1

        if int(wd_date_no) != int(wd_diary_no):
            raise ValidationError(
                u"No se puede salvar el curso porque la fecha de inicio ({}) cae en {}"
                u" y el primer dia de la agenda es {}.".format(
                    date_begin, date_begin_day, weekday))

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
    @api.depends('register_max', 'registration_ids')
    def _get_register(self):
        reg_current = reg_attended = reg_prospect = reg_cancel = 0

        for registration in self.registration_ids:
                # las que señaron o pagaron o estan cursando
            if registration.state == 'confirm' or registration.state == 'signed':
                reg_current += registration.nb_register
                # las que terminaron
            elif registration.state == 'done':
                reg_attended += registration.nb_register
                # las que estan interesadas
            elif registration.state == 'draft':
                reg_prospect += registration.nb_register
                # las que cancelaron
            elif registration.state == 'cancel':
                reg_cancel += registration.nb_register

        self.register_current = reg_current
        self.register_attended = reg_attended
        self.register_prospect = reg_prospect
        self.register_cancel = reg_cancel
        # the number of vacants is unlimited if the curso.register_max field is not set.
        # In that case we arbitrary set it to 9999, it is used in the
        # kanban view to special case the display of the 'subscribe' button
        self.register_avail = self.register_max - reg_current if self.register_max != 0 else 9999

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
    @api.onchange('diary_ids')
    @api.depends('date_begin', 'curso_instance', 'product.name','diary_ids')
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
        hhs = mms = hhe = mme = 0
        for diary_line in self.diary_ids.search([('curso_id', '=', self.id)]):
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

    @api.one
    def button_generate_lectures(self):
        """ Generar las clases que correspondan a este curso
        """
        date_begin = datetime.strptime(self.date_begin, '%Y-%m-%d')
        tot_hs_lecture = self.tot_hs_lecture
        hs_lecture = self.hs_lecture
        #        default_code = self.default_code
        if (operator.mod(tot_hs_lecture, hs_lecture) != 0):
            raise Warning(
                'Error!',
                u"la cantidad de horas catedra no es divisible por las horas de clase!.")

        no_lectures = int(tot_hs_lecture // hs_lecture)
        weekload = self.get_weekload()

        if (weekload == []):
            raise Warning('Error!', u"No se definió la agenda!.")

        # get lecture templates
        lecture_templates = self.get_lecture_templates(self.product.id)

        # get a lectures list or an exception if overlaps.
        seq = 1
        lectures = []
        for date, schedule, room in self.lectures_list(
                self.weekdays(weekload, date_begin), no_lectures):
            if not self.lecture_overlaps(date, schedule, room):
                lectures.append(
                    {'date': date,
                     'schedule': schedule,
                     #                         'room': room,
                     'curso': self,
                     'seq': seq}
                )
                seq += 1
            else:
                raise Warning(
                    'Error!',
                    u'La clase del %s en el horario %s y en el aula %s se superpone con una ya existente',
                    date, schedule.name, room)

        if len(lectures) != len(lecture_templates):
            raise Warning(
                'Error!',
                u'La cantidad de clases no coincide con la cantidad de contenidos.')

        lecs = []
        for ix, lec in enumerate(lectures):
            lec['date'] = lectures[ix]['date']
            lec['name'] = lecture_templates[ix]['name']
            lec['curso_id'] = lectures[ix]['curso'].id
            lec['schedule_id'] = lectures[ix]['schedule'].id
            lec['date_start'] = lectures[ix]['schedule'].start_datetime(lec['date'])
            lec['date_stop'] = lectures[ix]['schedule'].stop_datetime(lec['date'])
            lec['seq'] = lectures[ix]['seq']
            lecs.append(lec)

        # Add lectures
        lectures = self.env['curso.lecture'].search([('curso_id', '=', self.id)])
        for lecture in lectures:
            lecture.unlink()

        for lec in lecs:
            lectures.create(lec)

    @api.one
    @api.constrains('register_max', 'register_avail')
    def _check_seats_limit(self):
        if self.register_max and self.register_avail < 0:
            raise Warning('No hay mas vacantes.')

    @api.one
    def button_curso_confirm(self):
        """ Confirmar curso chequeando antes que tenga fecha de inicio y que coincida con la agenda
        """
        # Verificar si tiene fecha de inicio.
        if not (self.date_begin):
            raise ValidationError(u"No se puede confirmar el curso porque no tiene "
                                  u"fecha de inicio.")

        if not self.diary_ids:
            raise ValidationError(u"No se puede confirmar el curso porque no tiene "
                                  u"agenda creada.")

        if self.email_confirmation_id:
            # send reminder that will confirm the event for all the people that were already confirmed
            regs = self.registration_ids.filtered(
                lambda reg: reg.state not in ('draft', 'cancel'))
        # regs.mail_user_confirm()
        self.state = 'confirm'

    @api.one
    def button_curso_draft(self):
        self.state = 'draft'
