# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------------
from openerp import models, fields, api

class html_filter(models.TransientModel):
    """ genera html para varios propositos """

    dummy = fields.Char()

    def default_footer(self):
        return """
                <br/>
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
