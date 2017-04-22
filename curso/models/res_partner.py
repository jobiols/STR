# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from datetime import datetime

from openerp import models, fields, api

from . import html_filter


class res_partner(models.Model):
    _inherit = 'res.partner'

    teacher = fields.Boolean(
            'Profesora',
            help="Poner el tilde si el contacto es una profesora.")

    # TODO Revisar cursos que son de una profesora?? ver si se usa en algun lado...
    curso_ids = fields.One2many(
            'curso.curso',
            'main_speaker_id',
            readonly=True
    )

    curso_registration_ids = fields.One2many(
            'curso.registration',
            'partner_id')

    groupon = fields.Boolean('Validado')

    assistance_id = fields.One2many(
            'curso.assistance',
            'partner_id',
            'Asistencias'
    )

    c_started = fields.Char(
            'Cursos iniciados',
            store=True,
            help=u"Cursos que la alumna inició, señandolo, pero que todavía no terminaron están "
                 u"todavía cursándolos",
            compute="_compute_curso_assistance"
    )

    c_finished = fields.Char(
            'Cursos terminados',
            store=True,
            help=u"Cursos que la alumna inició y que ya terminaron. La alumna tuvo asistencia"
                 u"completa en esos cursos",
            compute="_compute_curso_assistance"
    )

    c_incomplete = fields.Char(
            'Cursos incompletos',
            store=True,
            help=u"Cursos que la alumna inició y que ya terminaron. La alumna no tuvo asistencia"
                 u"completa en esos cursos",
            compute="_compute_curso_assistance"
    )
    recover_ids = fields.Char(
            'ids a recuperar',
            help=u'Ids de las clases que podría recuperar esta alumna, y que le mandamos por mail,'
                 u'se guarda aqui para evitar mandarle mails con informacion repetida'
    )

    @api.one
    def button_resend_recover_mail(self):
        self.recover_ids = 'Programado para reenviar mail de recuperatorios'

    @api.one
    @api.depends('curso_registration_ids')
    def _compute_curso_assistance(self):
        """ Calcula los cursos a los que asistió la alumna agrupados en tres categorías
        """
        started = []
        finished = []
        incomplete = []
        for reg in self.curso_registration_ids:
            if reg.state == 'confirm':
                started.append(reg.curso_id.curso_instance)
            if reg.state == 'done':
                finished.append(reg.curso_id.curso_instance)
            if reg.state == 'cancel':
                incomplete.append(reg.curso_id.curso_instance)

        self.c_started = ' '.join(started)
        self.c_finished = ' '.join(finished)
        self.c_incomplete = ' '.join(incomplete)

    @api.model
    def info_curso_html(self, default_code, price=True, discount=False):
        """ Genera página html con la información del curso y si price = True le agrega
            el precio y el boton de pago.
        """
        producto = self.env['product.product'].search(
                [('default_code', '=', default_code)])
        data = producto.info_curso_html_data() or {}
        html = html_filter.html_filter()

        ret = html.default_header(data)
        ret += html.info_curso(data, price=price, discount=discount)
        ret += html.inicios_curso(data)
        return ret

    @api.model
    def info_recover_html(self, default_code):
        """ Genera tabla html con la información de recuperatorios para el curso
            default_code
            Es llamada desde la plantilla con el curso como parámetro
        """

        # obtener las clases futuras para este curso, que tienen vacantes
        lectures = self.env['curso.lecture'].search(
                [
                    ('default_code', '=', default_code),
                    ('date', '>', datetime.today().strftime('%Y-%m-%d'))
                ], order="seq, date")

        data = []
        for lecture in lectures:
            # valida para recuperar si tiene al menos una vacante
            if lecture.reg_vacancy > 0:
                data.append({
                    'code': lecture.curso_id.curso_instance,
                    'date': datetime.strptime(lecture.date, '%Y-%m-%d').strftime(
                            '%d/%m/%Y'),
                    'day': lecture.weekday,
                    'schedule': lecture.schedule_id.name,
                    'lecture_no': lecture.seq,
                    'vacancy': lecture.reg_vacancy,
                })

        html = html_filter.html_filter()
        return html.info_recover_html(data)

    @api.model
    def info_recover_html1(self):
        """ Genera tabla html con la información de recuperatorios para la alumna
            Es llamada desde la plantilla
            Las vacantes que muestra son solo para recuperacion.
        """

        for rec in self:

            # ids de las clases en las que puede recuperar
            ids = self.env['curso.assistance'].get_recover_ids(rec)

            # obtener el recordset con las clases
            lectures = self.env['curso.lecture'].browse(ids)

            data = []
            for lecture in lectures:
                data.append({
                    'code': lecture.curso_id.curso_instance,
                    'date': datetime.strptime(lecture.date, '%Y-%m-%d').strftime(
                            '%d/%m/%Y'),
                    'day': lecture.weekday,
                    'schedule': lecture.schedule_id.name,
                    'lecture_no': lecture.seq,
                    'vacancy': lecture.reg_vacancy_rec,
                })

            for da in data:
                print da['code'], da['lecture_no'], da['date'], da['vacancy']

            html = html_filter.html_filter()
            return html.info_recover_html(data)

    @api.multi
    def get_mail_footer_html(self):
        html = html_filter.html_filter()
        return html.default_footer()

    @api.multi
    def get_product_price_html(self, default_code_list):
        products = []
        for default_code in default_code_list:
            product = self.env['product.product'].search([('default_code', '=', default_code)])
            products.append({
                'default_code': product.default_code or '',
                'name': product.name or 'No existe el producto',
                'list_price': product.list_price}
            )

        html = html_filter.html_filter()
        return html.get_product_price(products)

    @api.multi
    def get_birthdate(self):
        return datetime.strptime(
                self.date, '%Y-%m-%d').strftime('%d/%m/%Y') if self.date else False

    @api.multi
    def get_info(self):
        for reg in self:
            ret = []
            if not reg.document_number:
                ret.append(u'Documento')
            if not (reg.mobile or reg.phone):
                ret.append(u'Teléfono')
            if not reg.date:
                ret.append(u'Cumpleaños')
            if reg.function and not reg.groupon:
                ret.append(u'Groupon sin validar')
            if not reg.email:
                ret.append(u'Email')
            if reg.credit > 0:
                ret.append(u'Nos debe ${}'.format(reg.credit))
            return ', '.join(ret)

    @api.multi
    def check_changed_info(self, recover_ids):
        """
            Ver si cambió la información a mandarle, si no cambió o tengo una lista vacia o sea no hay
            información que mandar, retorno falso para que no mande el mail.

        :param recover_ids: Lista con los ids de las clases donde puede recuperar
        :return: True si hay que mandarle el mail
        """
        self.ensure_one()
        ret = False
        print '2) check changed info --------------------------------------------------'

        # si no hay info que mandarle devuelvo false
        if not recover_ids:
            return False

        print '2.1 --- self={} len={}'.format(self, len(self))

        # pasar la lista a string para compararla con la guardada
        for rec in self:
            print '2.2 ------------------------------------------------------------------'  # , rec.name
            ri = ','.join(str(e) for e in recover_ids)
            print '2.3 {} -> {}'.format(ri, rec.recover_ids)
            if ri != rec.recover_ids:
                rec.recover_ids = ri
                # hay nueva información que mandar
                ret = True
            else:
                # no hay nueva información para mandar
                ret = False

        return ret

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
