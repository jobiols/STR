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

class html_filter:
    """ genera html para varios propositos
    """
#-----------------------------------------------------------------------------------------
    def default_header(self, data):
        """ Header de la pagina de información de curso
        """

        # hacemos que las imagenes sean responsives
        ret = u"""
<head>
    <style>
          img {
            max-width: 100%;
            height: auto;
        }
    </style>
</head>
        """

        # título del curso
        ret += u"""
<br/>
<h2>{} <a href="{}" style="font-size: 13px;" >Conocer más</a> </h2>
        """.format(data.get('name'), data.get('product_url'))

        # Descripción del curso
        ret += u'{}'.format(data.get('description'))
        return ret

#-----------------------------------------------------------------------------------------
    def default_footer(self):
        """ Footer de la página
        """

        #TODO parametrizar esto.
        return u"""
<br/>
<span style="font-family: lucida sans unicode,lucida grande,sans-serif;
    font-size: 20px;color: #ff0000;">
    <strong>Makeover Lab</strong>
</span><br />
Avda Rivadavia 5259 9° "34", Caballito<br />
Teléfono: 11 4902 4652<br />
Horario de atenciónón al público:<br />
Lunes a Viernes de 17 a 20 hs.<br />
Sábados de 11 a 19 hs<br />
<a href="https://www.facebook.com/MakeoverLabs">face/makeoverlabs</a><br />
<a href="http://www.makeoverlab.com.ar">www.makeoverlab.com.ar</a>
                """

#-----------------------------------------------------------------------------------------
    def info_curso(self, data, col=2, price=False):
        """ datos comerciales del curso
        """
        ret = u'<br/>'
        # para mails, aca puede o no ir el precio
        if col==2:
            ret += u"""
<table style="width: 100%;">
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
            dta = data.get('curso_data')
            for itm in dta:
                ret += u'       &nbsp;&nbsp;{}<br/>'.format(itm)
            ret += u"""
                </p>
            </td>
        </tr>
    </tbody>
</table>
<br/>


            """
            if price:
                ret += """
<h2>Valor del curso {} &nbsp;&nbsp; <a href="{}">Pagar ahora con Mercadopago</a></h2>
                """.format(data.get('curso_price'),data.get('mercadopago_button'))


        # para página web donde no entran dos columnas, aca no va el precio nunca
        else:
            ret += u"""
<table style="width: 550px;">
    <tbody>
        <tr>
            <td valign="top">
                <p style="border-left: 1px solid #8e0000; margin-left: 10px;">
            """
            for itm in data.get('comercial_data'):
                ret += u'       &nbsp;&nbsp;{}<br/>'.format(itm)
            dta = data.get('curso_data')
            for itm in dta:
                ret += u'       &nbsp;&nbsp;{}<br/>'.format(itm)
            ret += u"""
                </p>
            </td>
        </tr>
    </tbody>
</table>
<br/>
            """
        ret += u"""
<br />
<img src="http://makeoverlab.com.ar/wp-content/uploads/2016/10/mercadopago.png"
alt="Mercadopago"
width="394" height="200" />
            """
        return ret

#-----------------------------------------------------------------------------------------
    def inicios_curso(self, data):
        """ Inicios de nuevos cursos
        """

        ret = u'<br/><h2>Nuevos Inicios</h2>'

        for instance in data.get('instances', []):
            ret += u"""
    <div style="height: auto;margin-left:12px;margin-top:30px;">
        <table>
            <tbody>
            <tr>
                <td>
                    <div style="border-top-left-radius:3px;border-top-right-radius:3px;
                    border-collapse:separate;text-align:center;
                    font-weight:bold;color:#ffffff;width:100px;min-height: 17px;
                    border-color:#ffffff;background:#8a89ba;padding-top: 3px;">
                        {}
                    </div>
                    <div style="font-size:30px;min-height:35px;font-weight:bold;
                    line-height: 35px;text-align:center;color: #5F5F5F;
                    background-color: #E1E2F8;width: 100px;">
                        {}
                    </div>
                    <div style="font-size:11px;text-align:center;font-weight:bold;
                    color:#ffffff;background-color:#8a89ba">
                        {}
                    </div>
                    <div style="border-collapse:separate;color:#8a89ba;text-align:center;
                    width: 98px;font-size:11px;border-bottom-right-radius:3px;
                    font-weight:bold;border:1px solid;border-bottom-left-radius:3px;">
                        {}
                    </div>
                </td>
                <td>
                    <table border="0" cellpadding="0" cellspacing="0"
                           style="margin-top: 15px; margin-left: 10px;">
                        <tbody>
                        <tr>
                            <td style="vertical-align:top;">Días de cursada {} en el
                                horario de {}
                            </td>
                        </tr>
                        <tr>
                            <td style="vertical-align:top;">{}</td>
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
                """.format(instance.get('weekday'),
                           instance.get('day'),
                           instance.get('month'),
                           instance.get('curso_instance'),
                           instance.get('weekday'),
                           instance.get('schedule'),
                           data.get('mode'),
                           instance.get('vacancy'),
                           )
        ret += u'<br/>'
        return ret

#-----------------------------------------------------------------------------------------
    def diary_table(self):
        """ Genera el calendario de clases en html """
        return False

#-----------------------------------------------------------------------------------------
    def temario_curso(self, data):
        if data['temario']:
            ret = '<br/>'
            ret += "<h2>Temario</h2>"
            ret += data['temario']
        return ret

#-----------------------------------------------------------------------------------------
    def entrega_certificado(self, data):
        return """
<h4 style="text-align: center;">Se entrega certificado</h4>

<p style="text-align: center;">
    <img src="http://makeoverlab.com.ar/wp-content/uploads/2015/09/diplomas_final_curvas-e1469584463484.jpg"
    width="300"
    height="212"
    alt="Se entrega certificado del curso" />
</p>
        """


#-----------------------------------------------------------------------------------------
    def info_recover_html(self, data):
        """ Formatea los datos que vienen en data para generar una tabla que se insertará
            en una plantilla de mail (recuperatorios)
        """
        ret = u"""
<table border="0" cellpadding="0" cellspacing="0" dir="ltr">
    <tbody>
        <tr>
            <td style="width:55px"><strong>Cód</strong></td>
            <td style="width:80px"><strong>Fecha</strong></td>
            <td style="width:65px"><strong>Día</strong></td>
            <td style="width:125px"><strong>Horario</strong></td>
            <td><strong>Clase</strong></td>
        """
        for line in data:
            ret += u"""
        <tr>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
        </tr>
            """.format( line['code'],
                        line['date'],
                        line['day'],
                        line['schedule'],
                        line['lecture_no'])
        ret += u"""
		</tr>
	</tbody>
</table>
        """
        return ret

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
