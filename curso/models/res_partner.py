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

    curso_ids = fields.One2many(
        'curso.curso', 'main_speaker_id', readonly=True)

    curso_registration_ids = fields.One2many(
        'curso.registration', 'partner_id')

    def info_curso_html(self, default_code):
        producto = self.env['product.product'].search(
            [('default_code', '=', default_code)])
        data = producto.info_curso_html_data()
        data = data or {}
        html = html_filter.html_filter()

        ret = html.default_header(data)
        ret += html.info_curso(data)
        ret += html.inicios_curso(data)
        return ret

    @api.multi
    def get_mail_footer_html(self):
        html = html_filter.html_filter()
        return html.default_footer()

    @api.multi
    def get_birthdate(self):
        return datetime.strptime(
            self.date, '%Y-%m-%d').strftime('%d/%m/%Y') if self.date else False

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
