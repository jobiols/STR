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
from datetime import datetime, timedelta
from openerp import models, fields, api
import babel.dates


class curso_registration(models.Model):
    _name = 'curso.registration'
    _inherit = 'curso.registration'
    _order = 'create_date desc'
    _description = 'Inscripcion en cursos'


    create_date = fields.Date(
        u'Creación', readonly=True)

    date_closed = fields.Date(
        'Fecha de cierre', readonly=True)

    date_open = fields.Date(
        u'Fecha de inscripción', readonly=True)

    discount = fields.Float(
        'Descuento (%)', digits=(2, 2))

    disc_desc = fields.Char(
        'Razon del descuento', size=128, select=True)

    nb_register = fields.Integer(
        'Number of Participants', required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=1)

    state = fields.Selection(
        [('draft', u'Interesada'),
         ('cancel', u'Cancelado'),
         ('confirm', u'Cursando'),
         ('done', u'Cumplido'),
         ('signed', u'Señado')], 'Estado',
        track_visibility='onchange',
        size=16, readonly=True, default='draft')

    quota_id = fields.One2many(
        'curso.quota',
        'registration_id',
        'Cuotas')

    log_ids = fields.One2many(
        'mail.message',
        'res_id',
        'Logs',
        domain=[('model', '=', _name)])

    curso_id = fields.Many2one(
        'curso.curso',
        'Curso', required=True, readonly=True,
        states={'draft': [('readonly', False)]})

    partner_id = fields.Many2one(
        'res.partner',
        'Alumna',
        required=True,
        states={'done': [('readonly', True)]})

    user_id = fields.Many2one(
        'res.users', 'User',
        states={'done': [('readonly', True)]})

    reply_to = fields.Char(
        related='curso_id.reply_to',
        string='Reply-to Email',
        size=128,
        readonly=True)

    curso_begin_date = fields.Date(
        related='curso_id.date_begin',
        string="Inicio", readonly=True)

    email = fields.Char(
        related='partner_id.email', string='Email',
        size=128, readonly=True)

    phone = fields.Char(
        related='partner_id.mobile', string='Telefono',
        size=128, readonly=True)

    curso_state = fields.Selection(
        related='curso_id.state',
        string='Estado del curso', readonly=True)

    company_id = fields.Many2one(
        'res.company', string='Company', related='curso_id.company_id',
        store=True, readonly=True, states={'draft': [('readonly', False)]})

    curso_begin_day = fields.Char(
        compute='_get_weekday',
        string='Dia')

    @api.one
    @api.depends('curso_begin_date')
    def _get_weekday(self):
        try:
            init = datetime.strptime(self.curso_begin_date, "%Y-%m-%d")
        except:
            weekday = '???'
        else:
            weekday = babel.dates.format_datetime(
                init, format='EEE', locale=self.env.context['lang'])

        self.curso_begin_day = weekday.capitalize()

    @api.one
    def button_reg_sign(self):
        print 'seña el curso ------------------------------------------------------'
        # La alumna seña el curso, eso la confirma en el mismo

        # poner la alumna como cliente
        self.partner_id.write({'customer': True})

        # generarle las cuotas
        self.button_gen_quotes()

        # señar la inscripción
        res = self.sign_registration()

        # notificarla por mail si el curso tiene el template
        if self.curso_id.email_registration_id:
            template = self.curso_id.email_registration_id
            print '??',template.name
            if template:
                print 'envia mail ------ ',template.name
                mail_message = template.send_mail(self.id)
                print 'msg enviado',mail_message

    @api.one
    def sign_registration(self):
        print 'señar la inscripción -------------------------------------------------'
        self.curso_id.message_post(
            body=(u'Nueva seña para el curso: %s.') % (
                self.partner_id.name or '',),
            subtype="curso.mt_curso_registration"
        )
        self.state = 'signed'

    @api.one
    @api.constrains('curso_id', 'state', 'nb_register')
    def _check_seats_limit(self):
        if self.curso_id.register_max and \
                        self.curso_id.register_avail < (
                self.nb_register if self.state == 'draft' else 0):
            raise Warning(('No hay mas vacantes.!'))

    @api.one
    def button_gen_quotes(self):
        print 'generar cuotas ----------------------------------------------------'
        def calculate_invoice_date(sourcedate, months):
            return sourcedate + timedelta(days=30 * (months))

        date = datetime.strptime(self.curso_begin_date, '%Y-%m-%d')
        for quota in range(1, self.curso_id.product.no_quotes + 1):
            print 'cuota ',quota
            quota_data = {
                'registration_id': self.id,
                'date': calculate_invoice_date(date, quota - 1),
                'quota': quota,
                'list_price': self.curso_id.product.list_price
            }
            self.env['curso.quota'].create(quota_data)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
