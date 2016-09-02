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
        <div style="background:rgb(211, 211, 211); padding-left: 5px; padding-right: 5px; padding-top: 5px; padding-bottom: 5px;">
        <h2>{} <a href="{}" style="font-size: 13px;" >Conocer más</a> </h2>
        """.format(data.get('name'),data.get('product_url'))

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
        </div>
        <br/>
        """

        ret += u'<h2 style="text-align:center;"><br/>Nuevos Inicios</h2><br/>'

        ret += u'<div style="background:rgb(211, 211, 211); padding-left: 5px; padding-right: 5px; padding-top: 5px; padding-bottom: 5px;">'
        if False:
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
                            color: rgb(224, 30, 38); line-height: 50px;"><strong>{}</strong></div>

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

        for instance in data.get('instances',[]):
            ret += u"""
                <div style="height: auto;margin-left:12px;margin-top:30px;">
                    <table>
                        <tbody>
                        <tr>
                            <td>
                                <div style="border-top-left-radius:3px;border-top-right-radius:3px;
                                font-size:11px;border-collapse:separate;text-align:center;
                                font-weight:bold;color:#ffffff;width:100px;min-height: 17px;
                                border-color:#ffffff;background:#8a89ba;padding-top: 4px;">
                                    {}
                                </div>
                                <div style="font-size:45px;min-height:auto;font-weight:bold;
                                text-align:center;color: #5F5F5F;background-color: #E1E2F8;width: 100px;">
                                    {}
                                </div>
                                <div style="font-size:11px;text-align:center;font-weight:bold;
                                color:#ffffff;background-color:#8a89ba">
                                    {}
                                </div>
                                <div style="border-collapse:separate;color:#8a89ba;text-align:center;
                                width: 100px;font-size:11px;border-bottom-right-radius:3px;
                                font-weight:bold;border:1px solid;border-bottom-left-radius:3px;">
                                    {}
                                </div>
                            </td>
                            <td>
                                <table border="0" cellpadding="0" cellspacing="0"
                                       style="margin-top: 15px; margin-left: 10px;font-size: 16px;">
                                    <tbody>
                                    <tr>
                                        <td style="vertical-align:top;">Se cursa los días {} en el
                                            horario de {}
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="vertical-align:top;">Son {} clases de {} horas c/u.</td>
                                    </tr>
                                    <tr>
                                        <td style="vertical-align:top;">{}</td>
                                    </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </div>
                """.format( instance.get('weekday'),
                            instance.get('day'),
                            instance.get('month'),
                            instance.get('curso_instance'),
                            instance.get('weekday'),
                            instance.get('schedule'),
                            data.get('no_lectures'),
                            data.get('hs_lecture'),
                            instance.get('vacancy'),
                        )
        ret += u'</div><br/>'
        return ret

    @api.multi
    def get_mail_footer_html(self):
        return """
                <p><span style="font-family:lucida sans unicode,lucida grande,sans-serif;
                    font-size:20px;">
                <span style="color:#FF0000;"><strong>Makeover Lab</strong></span></span><br/>
                Avda Rivadavia 5259 9&deg; &quot;34&quot;, Caballito<br/>
                Tel&eacute;fono: 11 4902 4652<br/>
                Horario de atenci&oacute;n al p&uacute;blico:<br/>
                Lunes a Viernes de 17 a 20 hs.<br/>
                S&aacute;bados de 11 a 19 hs<br/>
                <a href="https://www.facebook.com/MakeoverLabs">face/makeoverlabs</a><br/>
                <a href="http://www.makeoverlab.com.ar">www.makeoverlab.com.ar</a></p>
                """



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
