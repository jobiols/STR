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
from openerp import models, fields

class res_partner(models.Model):
    _inherit = 'res.partner'

    teacher = fields.Boolean(
        'Profesora',
        help="Poner el tilde si el contacto es una profesora.")

    curso_ids = fields.One2many(
        'curso.curso', 'main_speaker_id', readonly=True)

    curso_registration_ids = fields.One2many(
        'curso.registration', 'partner_id')

    def info_curso_html(self,default_code):
        producto = self.env['product.product'].search([('default_code','=',default_code)])
        for pr in producto:
            print pr.default_code, pr.name
        ret = u"""
        <table border="0" cellpadding="0" cellspacing="0">
            <tbody>
                <tr>
                    <td>
                    <h2>{}</h2>
                    </td>
                    <td>
                    <h5><sub>&nbsp;cod {}</sub></h5>
                    </td>
                </tr>
            </tbody>
        </table>

        <blockquote>
            <p>Regalate o regalá un curso de automaquillaje.</p>
        </blockquote>

        <p>Vení a disfrutar del día y aprendé a maquillarte! Animate a pasar una tarde distinta
        aprendiendo tips y consejos para verte más linda, maquillada como una profesional</p>

        <p>Modalidad: 4&nbsp;clases de 2 hs</p>

        <table border="0" cellpadding="0" cellspacing="0" style="width: 500px;">
            <tbody>
                <tr>
                    <td><strong>Inicio</strong></td>
                    <td><strong>Cód</strong></td>
                    <td><strong>Días de cursada</strong></td>
                    <td><strong>Horario</strong></td>
                </tr>
                <tr bgcolor="#E0ECF8">
                    <td><span>19/08/2016</span></td>
                    <td><span>G01/26</span></td>
                    <td><span>Viernes</span></td>
                    <td><span>16:00 - 18:00 (2hs)</span></td>

                </tr>
                <tr bgcolor="#E0ECF8">
                    <td><span>26/08/2016</span></td>
                    <td><span>G01/27</span></td>
                    <td><span>Viernes</span></td>
                    <td><span>18:30 - 20:30 (2hs)</span></td>
                </tr>
            </tbody>
        </table>

        <br>

        <ul>
            <li>Valor del curso $1200.</li>
            <li>Matricula bonificada.</li>
            <li>Se entrega certificado digital.</li>
            <li>Los materiales están incluidos en el valor del curso.</li>
        </ul>

        <p>Ver mas información en <a href="http://makeoverlab.com.ar/automaquillaje-2/">nuesro sitio</a></p>
        """.format(producto.name,default_code)
        return ret

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
