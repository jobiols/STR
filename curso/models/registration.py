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

from datetime import datetime, date, timedelta
import operator

from openerp.osv import fields, osv
from openerp import SUPERUSER_ID
import babel.dates


class curso_registration(osv.osv):
    def _get_weekday(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for registration in self.browse(cr, uid, ids, context=context):
            try:
                init = datetime.strptime(registration.curso_begin_date, "%Y-%m-%d")
            except:
                weekday = '???'
            else:
                weekday = babel.dates.format_datetime(init, format='EEE',
                                                      locale=context['lang'])
            res[registration.id] = weekday.capitalize()
        return res

    _name = 'curso.registration'
    _description = __doc__
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    # curso registration model
    _columns = {
        'id': fields.integer('ID'),
        'quota_id': fields.one2many('curso.quota', 'registration_id', 'Cuotas'),
        'curso_id': fields.many2one('curso.curso', 'Curso', required=True, readonly=True,
                                    states={'draft': [('readonly', False)]}),
        'partner_id': fields.many2one('res.partner', 'Alumna', required=True,
                                      states={'done': [('readonly', True)]}),
        'create_date': fields.date(u'Creación', readonly=True),
        'date_closed': fields.date('Fecha de cierre', readonly=True),
        'date_open': fields.date(u'Fecha de inscripción', readonly=True),
        'reply_to': fields.related('curso_id', 'reply_to', string='Reply-to Email',
                                   type='char', size=128,
                                   readonly=True, ),
        'log_ids': fields.one2many('mail.message', 'res_id', 'Logs',
                                   domain=[('model', '=', _name)]),
        'curso_begin_date': fields.related('curso_id', 'date_begin', type='date',
                                           string="Inicio", readonly=True),
        'curso_begin_day': fields.function(_get_weekday, string='Dia', method=True,
                                           store=False, type='char'),
        'user_id': fields.many2one('res.users', 'User',
                                   states={'done': [('readonly', True)]}),
        'company_id': fields.related('curso_id', 'company_id', type='many2one',
                                     relation='res.company',
                                     string='Company', store=True, readonly=True,
                                     states={'draft': [('readonly', False)]}),
        'state': fields.selection([('draft', u'Interesada'),
                                   ('cancel', u'Cancelado'),
                                   ('confirm', u'Cursando'),
                                   ('done', u'Cumplido'),
                                   ('signed', u'Señado')], 'Estado',
                                  track_visibility='onchange',
                                  size=16, readonly=True),
        'email': fields.related('partner_id', 'email', string='Email', type='char',
                                size=128, readonly=True),
        'phone': fields.related('partner_id', 'mobile', string='Telefono', type='char',
                                size=128, readonly=True),
        'discount': fields.float('Descuento (%)', digits=(2, 2)),
        'disc_desc': fields.char('Razon del descuento', size=128, select=True),

        # Related fields
        'curso_state': fields.related('curso_id', 'state', type='char',
                                      string='Estado del curso', readonly=True),

        # Deprecated fields
        'nb_register': fields.integer('Number of Participants', required=True,
                                      readonly=True,
                                      states={'draft': [('readonly', False)]}),
    }
    _defaults = {
        'nb_register': 1,
        'state': 'draft',
    }
    _order = 'create_date desc'

    def confirm_registration(self, cr, uid, ids, context=None):
        for reg in self.browse(cr, uid, ids, context=context or {}):
            self.pool.get('curso.curso').message_post(cr, uid, [reg.curso_id.id],
                                                      body=(
                                                               u'Nuevo inicio de curso: %s.') % (
                                                               reg.partner_id.name or '',),
                                                      subtype="curso.mt_curso_registration",
                                                      context=context)
        return self.write(cr, uid, ids, {'state': 'confirm'}, context=context)

    def sign_registration(self, cr, uid, ids, context=None):
        for reg in self.browse(cr, uid, ids, context=context or {}):
            self.pool.get('curso.curso').message_post(cr, uid, [reg.curso_id.id],
                                                      body=(
                                                               u'Nueva seña para el curso: %s.') % (
                                                               reg.partner_id.name or '',),
                                                      subtype="curso.mt_curso_registration",
                                                      context=context)
        return self.write(cr, uid, ids, {'state': 'signed'}, context=context)

    def button_reg_sign(self, cr, uid, ids, context=None):
        """ Boton senio el curso
        """
        curso_obj = self.pool.get('curso.curso')
        for register in self.browse(cr, uid, ids, context=context):
            curso_id = register.curso_id.id
            no_of_registration = register.nb_register
            curso_obj.check_registration_limits_before(cr, uid, [curso_id],
                                                       no_of_registration,
                                                       context=context)
        res = self.sign_registration(cr, uid, ids, context=context)

        self.button_gen_quotes(cr, uid, ids, context=None)
        #        self.mail_user(cr, uid, ids, context=context)
        return res

    def button_reg_confirm(self, cr, uid, ids, context=None):
        """ Boton empezo el curso
        """
        for reg in self.browse(cr, uid, ids, context=context or {}):
            self.pool.get('curso.curso').message_post(cr, uid, [reg.curso_id.id],
                                                      body=(
                                                               u'Nueva inscripción en el curso: %s.') % (
                                                               reg.partner_id.name or '',),
                                                      subtype="curso.mt_curso_registration",
                                                      context=context)
        return self.write(cr, uid, ids, {'state': 'confirm'}, context=context)

    def button_reg_draft(self, cr, uid, ids, context=None):
        """ Boton volver a interesada
        """
        for reg in self.browse(cr, uid, ids, context=context or {}):
            self.pool.get('curso.curso').message_post(cr, uid, [reg.curso_id.id],
                                                      body=(
                                                               u'Vuelve a interesarse: %s.') % (
                                                               reg.partner_id.name or '',),
                                                      subtype="curso.mt_curso_registration",
                                                      context=context)
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)

    def button_reg_done(self, cr, uid, ids, context=None):
        """ Boton Termino el curso
        """
        if context is None:
            context = {}
        today = fields.datetime.now()
        for registration in self.browse(cr, uid, ids, context=context):
            register_pool = self.pool.get('curso.quota')
            records = register_pool.search(cr, uid,
                                           [('registration_id', '=', registration.id),
                                            ('list_price', '=', 0)])
            if len(records) != 0:
                raise osv.except_osv(('Error!'), (
                    u"No puede terminar el curso porque tiene cuotas pendientes. \
                    Se debería cancelar, o cobrarle las cuotas"))

            if today >= registration.curso_id.date_begin:
                values = {'state': 'done', 'date_closed': today}
                self.write(cr, uid, ids, values)
            else:
                raise osv.except_osv(('Error!'),
                                     (u"Hay que esperar al dia de inicio del curso para \
                                     decir que lo terminó."))

        return True

    def button_reg_cancel(self, cr, uid, ids, context=None, *args):
        # Eliminar todas las cuotas pendientes para no seguir cobrandole
        for registration in self.browse(cr, uid, ids, context=context):
            id = registration.id
            register_pool = self.pool.get('curso.quota')
            records = register_pool.search(cr, uid, [('invoice_id', '=', None),
                                                     ('registration_id', '=', id)])
        register_pool.unlink(cr, uid, records, context=None)
        return self.write(cr, uid, ids, {'state': 'cancel'})

    def button_gen_quotes(self, cr, uid, ids, context=None, *args):
        for registration in self.browse(cr, uid, ids, context=context):
            registration_id = registration.id
            date = datetime.strptime(registration.curso_begin_date, '%Y-%m-%d')

        for quota in range(1, registration.curso_id.product.no_quotes + 1):
            quota_data = {
                'registration_id': registration_id,
                'date': calculate_invoice_date1(date, quota - 1),
                'quota': quota,
                'list_price': registration.curso_id.product.list_price
            }
            self.pool.get('curso.quota').create(cr, uid, quota_data, context=context)
        return True

    def mail_user(self, cr, uid, ids, context=None):
        """
        Send email to user with email_template when registration is done
        """
        for registration in self.browse(cr, uid, ids, context=context):
            if registration.curso_id.state == 'confirm' and registration.curso_id.email_confirmation_id.id:
                self.mail_user_confirm(cr, uid, ids, context=context)
            else:
                template_id = registration.curso_id.email_registration_id.id
                if template_id:
                    mail_message = self.pool.get('email.template').send_mail(cr, uid,
                                                                             template_id,
                                                                             registration.id)
        return True

    def mail_user_confirm(self, cr, uid, ids, context=None):
        """
        Send email to user when the curso is confirmed
        """
        for registration in self.browse(cr, uid, ids, context=context):
            template_id = registration.curso_id.email_confirmation_id.id
            if template_id:
                mail_message = self.pool.get('email.template').send_mail(cr, uid,
                                                                         template_id,
                                                                         registration.id)
        return True


        # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
