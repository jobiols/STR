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

from openerp.osv import fields, osv


class curso_registration(osv.osv):
    _name = 'curso.registration'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    def confirm_registration(self, cr, uid, ids, context=None):
        for reg in self.browse(cr, uid, ids, context=context or {}):
            self.pool.get('curso.curso').message_post(cr, uid, [reg.curso_id.id],
                                                      body=(
                                                               u'Nuevo inicio de curso: %s.') % (
                                                               reg.partner_id.name or '',),
                                                      subtype="curso.mt_curso_registration",
                                                      context=context)
        return self.write(cr, uid, ids, {'state': 'confirm'}, context=context)

    def button_reg_confirm(self, cr, uid, ids, context=None):
        """ Boton empezo el curso
        """
        for reg in self.browse(cr, uid, ids, context=context or {}):
            self.pool.get('curso.curso'). \
                message_post(cr, uid, [reg.curso_id.id],
                             body=(u'Nueva inscripción en el curso: %s.') % (
                                 reg.partner_id.name or '',),
                             subtype="curso.mt_curso_registration",
                             context=context)
        return self.write(cr, uid, ids, {'state': 'confirm'}, context=context)

    def button_reg_draft(self, cr, uid, ids, context=None):
        """ Boton volver a interesada
        """
        for reg in self.browse(cr, uid, ids, context=context or {}):
            self.pool.get('curso.curso').message_post(
                    cr, uid, [reg.curso_id.id],
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
        # verificar si tiene cuotas impagas
        for registration in self.browse(cr, uid, ids, context=context):
            register_pool = self.pool.get('curso.quota')
            records = register_pool.search(
                    cr, uid, [('registration_id', '=', registration.id),
                              ('list_price', '=', 0)])
            if len(records) != 0:
                raise osv.except_osv(('Error!'),
                                     u"No puede terminar el curso porque tiene cuotas pendientes. \
                                     Se debería cancelar la inscripción, o cobrarle las cuotas")

            if today >= registration.curso_id.date_begin:
                values = {'state': 'done', 'date_closed': today}
                self.write(cr, uid, ids, values)
            else:
                raise osv.except_osv(
                        'Error!',
                        u"Hay que esperar al dia de inicio del curso para decir que lo \
                        terminó.")

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
