# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution.
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>...
#
##############################################################################

from datetime import datetime

from openerp.osv import fields, osv
import markdown


def generate_html(dict):
    for data in dict:
        ret = u"""
        <table border='0' cellpadding='0' cellspacing='0'>
            <tbody>
                <tr>
                    <td><h2>%s</h2>
                    </td>
                    <td><h5><sub>&nbsp;cod %s</sub></h5>
                    </td>
                </tr>
           </tbody>
        </table>
        <div style="text-align: justify;">%s</div>
        <p>%s<br/>%s</p>

        <table  border='0' cellpadding='0' cellspacing='0' style='width: 500px;'>
        <tbody>
            <tr>
                <td><strong>Inicio</strong></td>
                <td><strong>Cód</strong></td>
                <td><strong>Días de cursada</strong></td>
                <td><strong>Horario</strong></td>
            </tr>

            """ % (
            data['titulo'], data['codigo'],
            data['description'],
            data['modalidad'], data['duracion'])

        for line in data['grid']:
            ret += "        <tr bgcolor='#E0ECF8'> "
            ret += "            <td><span>" + line['inicio'] + "</span></td> "
            ret += "            <td><span>" + line['instancia'] + "</span></td> "
            ret += "            <td><span>" + line['dias'] + "</span></td> "
            ret += "            <td><span>" + line['horario'] + "</span></td> "
            ret += "        </tr> "

        ret += u"""

        </tbody>
        </table>

        <br>

        """
        if data['temario']:
            ret += "<h2>Temario</h2>"
            ret += data['temario']

        ret += "<hr/>"

        ret += '\n\n\n\n'

        if False:
            ret += '<h3 style="text-align: left;">Aranceles</h3>'
            for data in dict:
                if data['cuotas'] == '1':
                    ss = data['cuotas'] + " cuota de $" + data['valor']
                else:
                    ss = data['cuotas'] + " cuotas de $" + data['valor'] + " c/u"

                ret += u'<p><strong>Matrícula: ' + data['matricula'] + '</strong><br />'
                ret += '<strong>Pagos: ' + ss + '</strong></p>'

        ret += """
        <table border="0" cellpadding="1" cellspacing="1" style="width: 100%;">
            <tbody>
                <tr>
                    <td>
                    <h3 style="text-align: left;">Se entrega certificado</h3>
                    <p style="text-align: center;"><img alt="" src="https://d3njjcbhbojbot.cloudfront.net/web/images/promos/cdp_cert_logo.png" style="width: 110px; height: 110px;" /></p>
                    <p style="text-align: center;">Materiales inclu&iacute;dos en el costo del curso.</p>
                    </td>
                </tr>
        </tbody>
        </table>
        <br>
        """
        return ret


class product_product(osv.osv):
    _inherit = 'product.product'  # Permite la herencia propiamente dicho del modulo product
    _columns = {
        'product_url': fields.char('URL del producto', size=200),
        'tot_hs_lecture': fields.integer('Horas catedra',
                                         help="Cantidad de horas que tiene el curso en total."),
        'hs_lecture': fields.integer('Horas de clase',
                                     help="Duración de cada una de las clases."),
        'agenda': fields.text('Tema'),
        'no_quotes': fields.integer('Cantidad de cuotas'),

        'default_reply_to': fields.char('Respuesta por defecto', size=64,
                                        help="El mail del organizador, que se pondra en \
                                        el campo de respuesta de todos los mails \
                                        enviados automaticamente en inscripciones \
                                        y confirmaciones de cursos."),
        'default_email_registration': fields.many2one('email.template',
                                                      'Mail de inscripcion',
                                                      help="Selecciona el mail de \
                                                      inscripcion que se enviara a la \
                                                      alumna"),
        'default_email_curso': fields.many2one('email.template', 'Mail de confirmacion',
                                               help="Selecciona el mail de confirmacion \
                                               que se enviara a la alumna en el momento \
                                               de la confirmacion"),
        'default_registration_min': fields.integer('Minimo de alumnas en el curso',
                                                   help="define la cantidad minima de \
                                                   alumnas para arrancar el curso. (Pone \
                                                   cero para no tener en cuenta la regla)"),
        'default_registration_max': fields.integer('Maximo de alumnas en el curso',
                                                   help="Define la cantidad maxima de \
                                                   alumnas que puede tener el curso. \
                                                   (Pone cero para no tener en cuenta \
                                                   la regla)"),
        'lecture_template_ids': fields.one2many('curso.lecture_template', 'product_id',
                                                'Clases'),

    }
    _defaults = {
        'default_registration_min': 0,
        'default_registration_max': 0,
        'no_quotes': 1,
        'default_reply_to': "makeoverlabinfo@gmail.com"
    }

    #    _sql_constraints = [('default_code_unique', 'unique (default_code)', 'ya hay un producto con esta referencia.')]

    def find_schedule(self, list, data):
        for l in list:
            if l['horario'] == data:
                return l
        return False

    def _get_formatted_diary(self, cr, uid, curso_id, context=None):
        """
        Devuelve una lista con las lineas del diario agrupadas por horario y ordenadas por dia.
        Si un horario se repite en varios dias pone coma entres los dias.
        """
        formatted_diary = []
        diary = []

        # bajar el diary completo a la lista diary
        diary_pool = self.pool.get('curso.diary')
        ids = diary_pool.search(cr, uid, [('curso_id', '=', curso_id)])  #
        for dl in diary_pool.browse(cr, uid, ids, context=context):
            diary.append({
                'weekday': dl.weekday,
                'weekday_name': dl.weekday_name,
                'schedule': dl.schedule.name,
                'seq': dl.seq
            })

        # recorrer diary agrupando por schedule
        for diary_line in diary:
            # obtengo una referencia a la linea
            fd_line = self.find_schedule(formatted_diary, diary_line['schedule'])
            if fd_line:
                # si existe el horario le agrego el día a la lista de dias
                fd_line['list_dias'].append(diary_line['weekday_name'])
            else:
                # no existe el horario agrego la linea
                formatted_diary.append(
                    {'list_dias': [diary_line['weekday_name']],
                     'horario': diary_line['schedule']
                     })

        # hacer la lista de dias formateada
        for fdl in formatted_diary:
            fdl['dias'] = ', '.join(fdl['list_dias'])

        return formatted_diary

    def _get_wordpress_data(self, cr, uid, ids, default_code, context=None):
        """
        Genera el html para pegar en wordpress, trae todas las instancias de cursos
        basadas en este producto.
        """
        prod_pool = self.pool['product.product']
        ids = prod_pool.search(cr, uid, [
            ('default_code', '=', default_code),
        ])
        data = {}
        for prod in prod_pool.browse(cr, uid, ids, context=context):
            curso_pool = self.pool.get('curso.curso')
            # traer cursos por default code, con fecha de inicio y en estado
            # draft o confirm
            ids = curso_pool.search(cr, uid, [
                ('default_code', '=', prod.default_code),
                ('date_begin', '<>', False),
                '|',
                ('state', '=', 'draft'),
                ('state', '=', 'confirm')
            ])
            grid = []
            for curso in curso_pool.browse(cr, uid, ids, context=context):
                formatted_diary = self._get_formatted_diary(
                    cr, uid, curso.id, context=None)
                for idx, fdline in enumerate(formatted_diary):
                    if idx == 0:
                        grid.append(
                            {'inicio': datetime.strptime(curso.date_begin,
                                                         '%Y-%m-%d').strftime('%d/%m/%Y'),
                             'instancia': curso.get_formatted_instance(curso.id),
                             'dias': fdline['dias'],
                             'horario': fdline['horario'],
                             })
                    else:
                        grid.append(
                            {'inicio': '',
                             'instancia': '',
                             'dias': fdline['dias'],
                             'horario': fdline['horario'],
                             })
                grid.append(
                    {'inicio': '&nbsp;',
                     'instancia': '&nbsp;',
                     'dias': '&nbsp;',
                     'horario': '&nbsp;',
                     })
                print 'clases x week >>>>>>>>>>>>', curso.classes_per_week
                try:
                    weeks = \
                        (prod.tot_hs_lecture / prod.hs_lecture) / curso.classes_per_week
                except:
                    weeks = "error!"

                # si está vacio trae False y da una excepcion en mark_down
                if not prod.agenda:
                    prod.agenda = ''
                if not prod.description:
                    prod.description = ''

                if weeks > 1:
                    duracion = u'Duración %s semanas, (%s hs)' % (
                        weeks, prod.tot_hs_lecture)
                    if curso.classes_per_week > 1:
                        modalidad = u'Modalidad: %s clases de %s hs por semana' % (
                            curso.classes_per_week, prod.hs_lecture)
                    else:
                        modalidad = u'Modalidad: una clase de %s horas por semana' % (
                            prod.hs_lecture)
                else:
                    duracion = ''
                    if curso.classes_per_week > 1:
                        modalidad = u'Modalidad: %s clases de %s hs' % (
                            curso.classes_per_week, prod.hs_lecture)
                    else:
                        modalidad = u'Modalidad: una clase de %s horas' % (
                            prod.hs_lecture)

                data = {
                    'titulo': prod.name,
                    'codigo': prod.default_code,
                    'description': markdown.markdown(prod.description),
                    'duracion': duracion,
                    'modalidad': modalidad,
                    'grid': grid,
                    'temario': markdown.markdown(prod.agenda),
                    'matricula': 'Bonificada',
                    'cuotas': str(prod.no_quotes),
                    'valor': str(prod.list_price),
                }

                if False:
                    print '------------------------------------------------- new'
                    print 'titulo           ', data['titulo']
                    print 'codigo           ', data['codigo']
                    print 'description      ', data['description']
                    print 'duracion         ', data['duracion']
                    print 'modalidad        ', data['modalidad']
                    for dd in data['grid']:
                        print 'grid-data    ', dd
                    print 'temario          ', data['temario']
                    print 'matricula        ', data['matricula']
                    print 'cuotas           ', data['cuotas']
                    print 'valor            ', data['valor']
                    print '-------------------------------------------------'

        return data

    def button_generate_doc(self, cr, uid, ids, context=None):
        """
        Generate wordpress (html) data for curso
        """
        for prod in self.browse(cr, uid, ids, context=context):
            data = self._get_wordpress_data(cr, uid, ids, prod.default_code,
                                            context=context)
            new_page = {
                'name': prod.name,
                'content': generate_html([data]),
            }
            # Borrar el documento si es que existe
            doc_pool = self.pool.get('document.page')
            records = doc_pool.search(cr, uid, [('name', '=', prod.name)])
            doc_pool.unlink(cr, uid, records)
            # Crear el documento
            self.pool.get('document.page').create(cr, uid, new_page, context=context)

        return True

    def button_generate_lecture_templates(self, cr, uid, ids, context=None):
        for product in self.browse(cr, uid, ids):
            no_clases = product.tot_hs_lecture / product.hs_lecture
            temp_obj = self.pool['curso.lecture_template']
            temp_obj.create_template(cr, uid, ids, no_clases)

        return True

        # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
