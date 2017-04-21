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
        ('unique_partner_per_class', 'unique (partner_id, lecture_id)',
         'Una alumna no puede aparecer dos veces en una clase')]

    _order = 'curso_instance, seq'

    future = fields.Boolean(
            'Futuro',
            help=u'La fecha de la clase está en el futuro',
            compute='_get_time_status'
    )
    past = fields.Boolean(
            'Pasado',
            help=u'La fecha de la clase está en el pasado',
            compute='_get_time_status'
    )
    notifications = fields.Integer(
            help=u'Cantidad de veces que se la notificó para que recupere esta clase'
    )
    lecture_id = fields.Many2one(
            'curso.lecture',
            string='Clase',
            help=u'Clase a la que pertenece este registro de asistencia',
            required=True,
    )
    seq = fields.Integer(
            'Clase',
            related='lecture_id.seq',
            store=True
    )
    partner_id = fields.Many2one(
            'res.partner',
            string=u'Alumna',
            help=u'Alumna a la que pertenece este registro de asistencia',
            required=True
    )
    state = fields.Selection([
        ('programmed', 'Programado'),
        ('absent', 'Ausente'),
        ('to_recover', 'Prog para recup'),
        ('present', 'Presente'),
        ('abandoned', 'Abandonado')],
            default='programmed',
            required=True,
            help='Programado - La alumna debe concurrir a esta clase\n' + \
                 'Ausente    - La alumna no concurrió a la clase o informó que no va a concurrir\n' + \
                 'Prog para recup. - Se programó una clase de recuperatorio para esta\n' + \
                 'Presente   - La alumna concurrió a la clase\n' + \
                 'Abandonado - La alumna abandonó el curso, el sistema deja de informarle fechas de recuperatorios.'
    )
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
            related='lecture_id.date',
            help="Fecha de la clase",
    )
    curso_instance = fields.Char(
            related='lecture_id.curso_id.curso_instance',
            store=True
    )

    @api.multi
    def add_atendee(self, partner_id, lecture_id, recover=False):
        """ Agrega una alumna a una clase puede ser de recuperatorio o no """

        # chequear que haya una vacante

        if recover:
            # si es recuperatorio debe haber una clase del mismo
            # curso y misma secuencia que esté en estado absent,
            # esa sería la clase que estamos recuperando, buscamos
            # esa clase y le cambiamos el estado a to_recover.

            to_recover = self.search([('partner_id', '=', partner_id.id),
                                      ('seq', '=', lecture_id.seq),
                                      ('state', '=', 'absent')])

            assert len(to_recover) == 1, 'ERROR: Debe haber solo una clase a recuperar'

            for rec in to_recover:
                rec.state = 'to_recover'

        self.env['curso.assistance'].create(
                {'partner_id': partner_id.id,
                 'lecture_id': lecture_id.id,
                 'state': 'programmed',
                 'recover': recover}
        )

    @api.multi
    def button_toggle_present(self):
        """ La profesora le pone o le saca el presente a la alumna """

        for reg in self:
            if reg.present:
                reg.state = 'programmed'
            else:
                reg.state = 'present'

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
            # resetear el contador de mails enviados.
            rec.notifications = 0

    @api.multi
    def button_go_to_recover(self):
        for rec in self:
            rec.state = 'to_recover'

    @api.multi
    def button_go_programmed(self):
        """ volvemos el registro a programado """
        for rec in self:
            rec.state = 'programmed'

    @api.multi
    def button_go_abandoned(self):
        for rec in self:
            rec.state = 'abandoned'

    @api.multi
    @api.depends('date')
    def _get_time_status(self):
        for rec in self:
            # si la fecha viene en false pongo una en el pasado para que no reviente.
            rec.future = datetime.today().date() < datetime.strptime(rec.date or '2000-01-01', '%Y-%m-%d').date()
            rec.past = datetime.today().date() > datetime.strptime(rec.date or '2000-01-01', '%Y-%m-%d').date()

    @api.multi
    def get_recover_ids(self, partner_id):
        """ dada una alumna devolver los ids de las clases de recuperatorio """

        # averiguar a que clases faltó esta alumna
        absent_lectures = self.env['curso.assistance'].search(
                [('partner_id', '=', partner_id.id),
                 ('state', '=', 'absent')])

        # obtener los cursos y clases para proponer recuperatorio
        lectures_obj = self.env['curso.lecture']
        ret = []
        for al in absent_lectures:
            default_code = al.lecture_id.curso_id.default_code  # que curso tiene que recuperar
            seq = al.lecture_id.seq  # que numero de clase tiene que recuperar

            # averiguar que clases hay para ese curso y numero de clase y que estan en el futuro
            candidate_lectures = lectures_obj.search([('default_code', '=', default_code),
                                                      ('seq', '=', seq),
                                                      ('next', '=', True)])
            for cl in candidate_lectures:
                # agregar solo clases que tengan al menos una vacante
                if cl.reg_vacancy > 0:
                    ret.append(cl.id)

        return ret

    @api.multi
    def send_notification_mail(self, partner_id):
        """ Arma el mail para recuperatorios """
        print '3) send notification mail -------------------------------',
        print 'a este partner', partner_id.name

        # Obtener el template para mandarle el mail,
        # En assistance estan los ausentes, me traigo los ausentes de este partner
        # Si encuentro ausentes en el futuro también valen y les busco recuperatorio.
        assistance = self.env['curso.assistance'].search([
            ('partner_id', '=', partner_id.id),
            ('state', '=', 'absent')])

        # Anoto todos los templates que hay que mandarle, habrá uno por cada curso
        template_ids = []
        print 'detecto ausencia en estas clases -----------------------------------------'
        for rec in assistance:
            print ' >>> ', rec.curso_instance, rec.seq, rec.lecture_id.name
            if rec.lecture_id.curso_id.email_recovery_id not in template_ids:
                template_ids.append(rec.lecture_id.curso_id.email_recovery_id)

        # por cada template, mandar un mail
        for template in template_ids:
            print 'template name [{}]'.format(template.name)
#            mail_message = template.send_mail(partner_id.id)
            print 'mail enviado ==========================='
            partner_id.info_recover_html1()
            print ' '

    @api.multi
    def do_run_housekeeping(self):
        print '1) do_run_houskeeping -------------------------------------------'

        # obtener las que faltaron y ponerles ausente
        # no se puede poner past en el dominio porque no puede ser stored=True
        assistance = self.env['curso.assistance'].search([('state', '=', 'programmed')])
        for rec in assistance:
            if rec.past:
                rec.state = 'absent'

        # Buscar los ausentes para mandarles mail de recuperatorio
        assistance = self.env['curso.assistance'].search([('state', '=', 'absent')])
        for rec in assistance:
            if rec.partner_id.check_changed_info(self.get_recover_ids(rec.partner_id)):
                self.send_notification_mail(rec.partner_id)

                # anotar que se la notificó otra vez para abandonar si pasa los 2
                rec.notifications += 1
                if rec.notifications > 2000:
                    rec.state = 'abandoned'

    def run_housekeeping(self, cr, uid, context=None):
        """ Chequea los ausentes y manda mails (si no le pongo esta firma no lo llama
            desde el cron)
        """

        self.do_run_housekeeping(cr, uid, context)
        return True
