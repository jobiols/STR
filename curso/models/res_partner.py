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

    def info_curso_html(self, default_code):
        producto = self.env['product.product'].search(
            [('default_code', '=', default_code)])
        data = producto.info_curso_html_data()
        data = data or {}
        ret = u'<table border="0" cellpadding="0" cellspacing="0">'
        ret += u'   <tbody>'
        ret += u'       <tr>'
        ret += u'           <td>'
        ret += u'               <h2>{}</h2>'.format(data.get('title'))
        ret += u'           </td>'
        ret += u'           <td>'
        ret += u'               <h5><sub>&nbsp;cod {}</sub></h5>'.format(data.get('code'))
        ret += u'           </td>'
        ret += u'           <td>'
        ret += u'               <h3>&nbsp;&nbsp;<a'
        ret += u'               href="{}">Conocer más</a></h3>'.format(
            data.get('product_url'))
        ret += u'           </td>'
        ret += u'       </tr>'
        ret += u'   </tbody>'
        ret += u'</table>'

        ret += u'<div style="width: 550px;">'
        ret += data.get('description')
        ret += u'</div>'

        ret += u'<table style="width: 550px;">'
        ret += u'<tbody>'
        ret += u'    <tr>'
        ret += u'        <td valign="top">'
        ret += u'            <p style="border-left: 1px solid #8e0000; margin-left: 10px;">'
        for itm in data.get('comercial_data'):
            ret += u'                    &nbsp;&nbsp;{}.<br/>'.format(itm)
        ret += u'            </p>'
        ret += u'        </td>'
        ret += u'        <td>&nbsp;&nbsp;</td>'
        ret += u'        <td valign="top">'
        ret += u'            <p style="border-left: 1px solid #8e0000; margin-left: 10px;">'
        for itm in data.get('curso_data'):
            ret += u'                    &nbsp;&nbsp;{}.<br/>'.format(itm)
        ret += u'            </p>'
        ret += u'        </td>'
        ret += u'    </tr>'
        ret += u'</tbody>'
        ret += u'</table>'

        ret += u'<h3>Nuevos Inicios</h3>'

        ret += u'<table style="width:550px;">'
        ret += u'<tbody>'
        for instance in data.get('instances',[]):
            ret += u'<tr>'
            ret += u'   <td style="text-align: center; color: rgb(224, 30, 38); bgcolor: rgb(200,100,00);">'
            ret += u'       <p><span style="align: center; font-size: 10.8px; '
            ret += u'       text-transform: uppercase;">{}</span><br/>'.format(instance.get('month'))
            ret += u'       <span style="font-size: 45px; font-family: Oswald, sans-serif; '
            ret += u'       ">{}</span></p></td>'.format(instance.get('day'))
            ret += u'   <td style="padding-right:10px">&nbsp;</td>'
            ret += u'   <td style="padding-right:10px" align="top">'
            ret += u'       <p> <strong>{}</strong> -'.format(instance.get('name'))
            ret += u'       Se dicta los días {} en el horario de {}<br/>'.format(instance.get('weekday'),instance.get('schedule'))
            ret += u'       {}</p>'.format(instance.get('vacancy'))
            ret += u'   </td>'
            ret += u'   <td style="text-align: center;">'
            ret += u'       <span style="font-size: 20px; font-family: Oswald, sans-serif; color: rgb(0, 0, 0);'
            ret += u'       line-height: 30px;">'
            ret += u'       ${} <br/> /mes</span>'.format(instance.get('price'))
            ret += u'   </td>'
            ret += u'</tr>'
        ret += u'</tbody>'
        ret += u'</table>'
        print ret
        return ret

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
