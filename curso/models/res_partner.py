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

    # TODO Revisar cursos que son de una profesora??
    curso_ids = fields.One2many(
        'curso.curso',
        'main_speaker_id',
        readonly=True)

    curso_registration_ids = fields.One2many(
        'curso.registration',
        'partner_id')

    groupon = fields.Boolean('Validado')

    @api.model
    def info_curso_html(self, default_code, price=True):
        """ Genera página html con la información del curso y si price = True le agrega
            el precio y el boton de pago.
        """
        producto = self.env['product.product'].search(
            [('default_code', '=', default_code)])
        data = producto.info_curso_html_data() or {}
        html = html_filter.html_filter()

        ret = html.default_header(data)
        ret += html.info_curso(data, price=price)
        ret += html.inicios_curso(data)
        return ret

    @api.model
    def info_recover_html(self, default_code):
        """ Genera tabla html con la información de recuperatorios para el curso
            default_code
        """
        producto = self.env['product.product'].search(
            [('default_code', '=', default_code)])
        data = producto.info_recover_html(default_code) or {}
        html = html_filter.html_filter()
        return html.info_recover_html(data)

    @api.multi
    def get_mail_footer_html(self):
        html = html_filter.html_filter()
        return html.default_footer()

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

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
