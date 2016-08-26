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
from openerp import models, fields, api

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
                    <td>
                        <h3>&nbsp;&nbsp;<a
                        href="{}">Conocer más</a></h3>
                    </td>
                </tr>
            </tbody>
        </table>""".format(data.get('name'),data.get('code'),data.get('product_url'))

        ret += u"""
        <div style="width: 550px;">{}</div>""".format(data.get('description'))

        ret += u"""
        <table style="width: 550px;">
            <tbody>
                <tr>
                    <td valign="top">
                        <p style="border-left: 1px solid #8e0000; margin-left: 10px;">
        """
        for itm in data.get('comercial_data'):
            ret += u'       &nbsp;&nbsp;{}<br/>'.format(itm)
        ret += u"""
                        </p>
                    </td>
                    <td>&nbsp;&nbsp;</td>
                    <td valign="top">
                        <p style="border-left: 1px solid #8e0000; margin-left: 10px;">
        """
        for itm in data.get('curso_data'):
            ret += u'       &nbsp;&nbsp;{}<br/>'.format(itm)
        ret += u"""
                        </p>
                    </td>
                </tr>
            </tbody>
        </table>
        """

        ret += u'<h3><br/>Nuevos Inicios</h3>'

        ret += u"""
        <table style="width:550px;">
            <tbody>
        """
        for instance in data.get('instances',[]):
            ret += u"""
            <tr>
                <td style="height:85px;">
                    <div style="  vertical-align: top;
                        border-radius: 15px 15px 15px 15px;
                        -moz-border-radius: 15px 15px 15px 15px;
                        -webkit-border-radius: 15px 15px 15px 15px; border: 0px solid #2b0f2b;
                        background-color: rgb(211, 211, 211); width: 70px; text-align: center;
                        border-right-color: rgb(255, 255, 255);">

                    <div style="box-sizing: border-box; font-size: 10px; color: rgb(224, 30, 38);
                        text-transform: uppercase;"><strong>{}</strong></div>

                    <div style="box-sizing: border-box; font-size: 40px; font-family: Oswald, sans-serif;
                        color: rgb(224, 30, 38); line-height: 50px;">{}</div>

                    <div style="box-sizing: border-box; font-size: 10px; color: rgb(224, 30, 38);
                        text-transform: uppercase;"><strong>{}</strong></div>
                    </div>
                </td>
                <td>&nbsp;&nbsp;</td>
                <td style="vertical-align:top">
                    <p>Se cursa los días {} en el horario de {}.
                       Son {} clases de {} horas c/u.
                    </p>
                    <p>código {} - {}</p>
                </td>
            </tr>""".format(instance.get('weekday'),
                            instance.get('day'),
                            instance.get('month'),
                            instance.get('weekday'),
                            instance.get('schedule'),
                            data.get('no_lectures'),
                            data.get('hs_lecture'),
                            instance.get('curso_instance'),
                            instance.get('vacancy'),
                            )
        ret += u"""
            </tbody>
        </table>
        """
        return ret

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
