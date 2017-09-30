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

    # -----------------------------------------------------------------------------------------
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
        ret += '<div style="max-width: 440px;">'
        ret += u'{}'.format(data.get('description'))
        ret += '</div>'
        return ret

    # -----------------------------------------------------------------------------------------
    def default_footer(self):
        """ Footer de la página
        """

        # TODO parametrizar esto.
        return u"""
<p><span style="font-size: 16px;">

<a href="http://makeoverlab.com.ar/wp-content/uploads/2017/09/Catalogo-de-Productos-Mila.pdf">Cat&aacute;logo Mila Marzi / Pro</a>
<br />

<a href="http://makeoverlab.com.ar/wp-content/uploads/2017/09/Catalogo-de-Productos-Visage.pdf">Cat&aacute;logo Pinceles Visage</a>
<br />

<a href="http://makeoverlab.com.ar/wp-content/uploads/2017/09/Catalogo-de-Productos-de-Farmacia-Once.pdf">Cat&aacute;logo Laboratorio Once</a><br /></span></p>

<table>
<tbody>
<tr>
<td><a href="https://www.facebook.com/MakeoverLabs/"><img src="http://makeoverlab.com.ar/wp-content/uploads/2017/02/social-facebook.png" alt="facebook" width="26" height="26" />&nbsp;Facebook</a>&nbsp;&nbsp;</td>
<td><a href="https://twitter.com/MakeoverLabs?lang=es"><img src="http://makeoverlab.com.ar/wp-content/uploads/2017/02/social-tweeter.png" alt="tweeter" width="26" height="26" />&nbsp;Tweeter</a>&nbsp;&nbsp;</td>
<td><a href="https://www.instagram.com/makeoverlabnavarre/"><img src="http://makeoverlab.com.ar/wp-content/uploads/2017/02/social-instagram.png" alt="instagram" width="26" height="26" />&nbsp;Instagram</a>&nbsp;&nbsp;</td>
<td><a href="https://ar.linkedin.com/in/analianavarre"><img src="http://makeoverlab.com.ar/wp-content/uploads/2017/02/social-linkedin.png" alt="linkedin" width="26" height="26" />&nbsp;Linkedin</a>&nbsp;&nbsp;</td>
</tr>
</tbody>
</table>
<table>
<tbody>
<tr>

<!--
<td><a href="makeoverlab.mitiendanube.com"><img src="http://makeoverlab.com.ar/wp-content/uploads/2017/02/social-tienda.png" alt="sitio web" width="26" height="26" />&nbsp;Nuestra tienda virtual</a>&nbsp;</td>
-->

<td><a href="http://www.makeoverlab.com.ar"><img src="http://makeoverlab.com.ar/wp-content/uploads/2017/02/social-web.png" alt="sitio web" width="26" height="26" />&nbsp;Nuestro Sitio web</a>&nbsp;</td>
</tr>
</tbody>
</table>

<p><br /> <span style="font-family: lucida sans unicode,lucida grande,sans-serif; font-size: 20px; color: #ff0000;"> <strong>Makeover Lab</strong> </span><br /><a href="http://www.makeoverlab.com.ar">www.makeoverlab.com.ar</a></p>
<p>Datos de contacto<br/>
Av Rivadavia 5512 Piso 1 Local "23" Galeria Comercial Caballito<br/>
Horario de atencion personalizada<br/>
Lunes a viernes de 16 a 20Hs Sabados 11 a 18Hs<br/>

<p>Telefono 11 3347 7058</p>
<p>Consultas y pedidos:<br /><a href="mailto:info@makeoverlab.com.ar">info@makeoverlab.com.ar</a></p>
            """

    # -----------------------------------------------------------------------------------------
    def info_curso(self, data, col=1, price=False, discount=False):
        """ datos comerciales del curso
        """
        ret = u'<br/>'
        # para mails, aca puede o no ir el precio
        if col == 2:
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
            if not discount:
                ret += """
<h2>Valor del curso ${} {} &nbsp;&nbsp; <br/>
<a href="{}">Pagar ahora con Mercadopago</a></h2>
                    """.format(data.get('curso_price'),
                               data.get('curso_price_per'),
                               data.get('mercadopago_button'))
            else:
                old_price = data['curso_price']
                discount = data.get('mercadopago_discount')
                new_price = int(round(old_price * discount / 100))
                ret += """
<h2>Valor del curso <s>${}</s>&nbsp; <span style="color:#FF0000;">Ahora ${}</span>&nbsp; <br/>
<a href="{}">Pagar con Mercadopago</a></h2>
                    """.format(old_price, new_price, data.get('mercadopago_button_discount'))
        # para página web donde no entran dos columnas
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

    # -----------------------------------------------------------------------------------------
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

    # -----------------------------------------------------------------------------------------
    def diary_table(self):
        """ Genera el calendario de clases en html """
        return False

    # -----------------------------------------------------------------------------------------
    def temario_curso(self, data):
        if data['temario']:
            ret = '<br/>'
            ret += "<h2>Temario</h2>"
            ret += data['temario']
        return ret

    # -----------------------------------------------------------------------------------------
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

    # -----------------------------------------------------------------------------------------
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
            <td><strong>Clase&nbsp;</strong></td>
            <td><strong>Vacantes</strong></td>
        """
        for line in data:
            ret += u"""
        <tr>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
        </tr>
            """.format(line['code'],
                       line['date'],
                       line['day'],
                       line['schedule'],
                       line['lecture_no'],
                       line['vacancy'])
        ret += u"""
        </tr>
    </tbody>
</table>
        """
        return ret if data else u"""<strong>Lamentablemente no disponemos de vacantes en este momento.</strong>"""

    def get_product_price(self, products):
        """ Formatea una linea de producto para hacer un pequeño catalogo
        """
        ret = u"""
<table>
"""
        for product in products:
            ret += u"""
    <tr>
            <td>
                {}&nbsp;&nbsp;
            </td>
            <td>
                {}&nbsp;&nbsp;
            </td>
            <td>
                ${:.2f}
            </td>
    </tr>
""".format(product['default_code'], product['name'], product['list_price'])
        ret += u"""
</table>
"""
        return ret

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
