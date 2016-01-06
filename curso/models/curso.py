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

from datetime import datetime, date, timedelta
import operator

from openerp.osv import fields, osv
from openerp import SUPERUSER_ID
import babel.dates


# class curso_type(osv.osv):
#    #    """ curso Type DEPRECATED!! """
#    _name = 'curso.type'
#    _description = __doc__
#    _columns = {
#    }

# def calculate_invoice_date(curso_date):
#    dd = datetime.strptime(curso_date, '%Y-%m-%d')
#
#    year = datetime.now().year
#    month = datetime.now().month
#    day = int(dd.strftime('%d'))
#    return datetime.strftime(date(year, month, day), '%Y-%m-%d')

def format_instance(default_code, instance):
    return '{}/{:0>2d}'.format(default_code, instance)


class curso_information(osv.osv_memory):
    """ Wizard para generar documentacion de los cursos
    """
    _name = 'curso.information'
    _description = __doc__

    def button_information(self, cr, uid, ids, context=None):
        curso_pool = self.pool.get('curso.curso')
        for curso in curso_pool.browse(cr, uid, context['active_ids'], context):
            curso.generate_doc_curso()
        return True


class curso_curso(osv.osv):
    """ Representa una instancia de un curso """
    _name = 'curso.curso'
    _description = __doc__
    _order = 'date_begin'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    class weekdays():
        _weekload = []

        def __init__(self, wl, date):
            self._weekload = wl
            self._start_day = date

            # Obtener el dia de la semana que empieza el curso
            self._start_weekday = self._start_day.weekday()

            # chequear con cada horario para ver si coincide con alguno
            self._current_ix = None
            for ix, rec in enumerate(self._weekload):
                if int(rec.get('weekday')) == self._start_weekday:
                    self._current_ix = ix
                    break

            if self._current_ix is None:
                raise osv.except_osv('Error!', (
                    u"La fecha de inicio no corresponde con Dia 1 ni con Dia 2"))

        def current_weekload(self):
            return self._weekload[self._current_ix]

        def next_delta(self):
            last_weekday = int(self._weekload[self._current_ix].get('weekday'))

            self._current_ix += self._current_ix
            if self._current_ix >= len(self._weekload):
                self._current_ix = 0

            current_weekday = int(self._weekload[self._current_ix].get('weekday'))
            delta = current_weekday - last_weekday

            if (delta == 0) and (self._current_ix == 0):
                delta = 7
            if delta < 0:
                delta += 7

            return delta

    def generate_doc_curso_html(self, dict):
        ret = ""
        ret += "  	<style type=\"text/css\">th"
        ret += "{"
        ret += "                background-color: white;"
        ret += "                color: black;"
        ret += "                text-align: center;"
        ret += "                vertical-align: bottom;"
        ret += "                height: 100px;"
        ret += "                padding-bottom: 3px;"
        ret += "                padding-left: 2px;"
        ret += "                padding-right: 2px;"
        ret += "            }"

        ret += "            .verticalText"
        ret += "            {"
        ret += "                text-align: center;"
        ret += "                vertical-align: middle;"
        ret += "                width: 18px;"
        ret += "                margin: 0px;"
        ret += "                padding: 0px;"
        ret += "                padding-left: 1px;"
        ret += "                padding-right: 1px;"
        ret += "                padding-top: 5px;"
        ret += "                white-space: nowrap;"
        ret += "                -webkit-transform: rotate(-90deg);"
        ret += "                -moz-transform: rotate(-90deg);"
        ret += "            };"
        ret += "</style>"

        ret += "<table border=\"1\">"
        ret += "	<tbody>"
        ret += "		<tr>"
        ret += "			<th width=\"200px;\">"
        ret += "			<div>" + dict['titulo'] + "</div>"
        ret += "			</th>"
        for clase in dict['clases']:
            ret += "			<th>"
            ret += "			<div class=\"verticalText\">" + clase['fecha'] + "</div>"
            ret += "			</th>"

        ret += "		</tr>"
        for alumna in dict['alumnas']:
            ret += "		<tr>"
            if alumna['state'] <> 'confirm':
                ret += "			<td>" + alumna['name'] + ' (Sin confirmar)' + "</td>"
            else:
                ret += "			<td>" + alumna['name'] + "</td>"

            for fecha in dict['clases']:
                ret += "			<td>&nbsp;</td>"

            ret += "		</tr>"

        ret += "	</tbody>"
        ret += "</table>"
        ret += "<h2><br/><br/>Temario</h2>"
        ret += "<table border=\"0\" cellpadding=\"1\" cellspacing=\"1\" style=\"width: 100%;\">"
        ret += "	<tbody>"
        for clase in dict['clases']:
            ret += "		<tr>"
            ret += "			<td>" + clase['fecha'] + "&nbsp;</td>"
            if clase['desc']:
                dd = clase['desc']
            else:
                dd = "no hay tema"
            ret += "			<td>" + dd + "</td>"
            ret += "		</tr>"
        ret += "</tbody>"
        ret += "</table>"

        return ret

    def generate_doc_curso(self, cr, uid, ids, context=None):
        for curso in self.browse(cr, uid, ids, context=context):
            alumnas = []
            reg_pool = self.pool.get('curso.registration')
            # mostrar las alumnas confirmada y señadas
            records = reg_pool.search(
                cr,
                uid,
                [
                    ('curso_id', '=', curso.id),
                    '|', ('state', '=', 'confirm'), ('state', '=', 'signed')
                ])
            for reg in reg_pool.browse(cr, uid, records, context=context):
                alumnas.append(
                    {'name': reg.partner_id.name,
                     'credit': reg.partner_id.credit,
                     'state': reg.state})

            clases = []
            lect_pool = self.pool.get('curso.lecture')
            records = lect_pool.search(cr, uid, [('curso_id', '=', curso.id)],
                                       order="date")
            for lect in lect_pool.browse(cr, uid, records, context=context):
                d = {
                    'fecha': datetime.strftime(
                        datetime.strptime(lect.date, "%Y-%m-%d"), "%d/%m/%y"),
                    'desc': lect.desc,
                }
                clases.append(d)

            data = {
                'titulo': curso.curso_instance,
                'alumnas': alumnas,
                'clases': clases,
            }

            new_page = {
                'name': curso.name,
                'content': self.generate_doc_curso_html(data),
            }

        # Borrar el documento si es que existe
        doc_pool = self.pool.get('document.page')
        records = doc_pool.search(cr, uid, [('name', '=', curso.name)])
        doc_pool.unlink(cr, uid, records)

        # Generar el documento
        self.pool.get('document.page').create(cr, uid, new_page, context=context)

        return True

    def name_get(self, cr, uid, ids, context=None):
        if not ids:
            return []

        if isinstance(ids, (long, int)):
            ids = [ids]

        res = []
        for record in self.browse(cr, uid, ids, context=context):
            curs = record.product.name
            display_name = record.name
            res.append((record['id'], display_name))
        return res

    def copy(self, cr, uid, id, default=None, context=None):
        """ Reset the state and the registrations while copying an curso
        """
        if not default:
            default = {}
        default.update({
            'state': 'draft',
            'registration_ids': False,
        })
        return super(curso_curso, self).copy(cr, uid, id, default=default,
                                             context=context)

    def button_draft(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)

    def button_cancel(self, cr, uid, ids, context=None):
        registration = self.pool.get('curso.registration')
        reg_ids = registration.search(cr, uid, [('curso_id', 'in', ids)], context=context)
        for curso_reg in registration.browse(cr, uid, reg_ids, context=context):
            if curso_reg.state != 'cancel':
                raise osv.except_osv('Error!',
                                     u"Para cancelar el curso debe cancelar todas \
                                     las alumnas.")
        registration.write(cr, uid, reg_ids, {'state': 'cancel'}, context=context)
        return self.write(cr, uid, ids, {'state': 'cancel'}, context=context)

    def button_done(self, cr, uid, ids, context=None):
        registration = self.pool.get('curso.registration')
        reg_ids = registration.search(cr, uid, [('curso_id', 'in', ids)], context=context)
        for curso_reg in registration.browse(cr, uid, reg_ids, context=context):
            if not ((curso_reg.state == 'done') or (curso_reg.state == 'cancel') or (
                        curso_reg.state == 'draft')):
                raise osv.except_osv(('Error!'), (
                    u"Para terminar el curso las alumnas deben estar en estado \
                    cumplido, cancelado o interesada."))
                #        registration.write(cr, uid, reg_ids, {'state': 'cancel'}, context=context)
        return self.write(cr, uid, ids, {'state': 'done'}, context=context)

    def check_registration_limits(self, cr, uid, ids, context=None):
        for self.curso in self.browse(cr, uid, ids, context=context):
            total_confirmed = self.curso.register_current
            if total_confirmed < self.curso.register_min or \
                                    total_confirmed > self.curso.register_max and \
                                    self.curso.register_max != 0:
                raise osv.except_osv('Error!', (
                    u"El total de inscripciones confirmadas para el curso '%s' no \
                    cumple con los requerimientos esperados de minimo/maximo. \
                    Reconsidere estos limites antes de continuar.") % (
                                         self.curso.name))

    def check_registration_limits_before(self, cr, uid, ids, no_of_registration,
                                         context=None):
        for curso in self.browse(cr, uid, ids, context=context):
            available_seats = curso.register_avail
            if available_seats and no_of_registration > available_seats:
                raise osv.except_osv('Cuidado!',
                                     u"Solo hay %d vacantes disponnibles!" %
                                     available_seats)
            elif available_seats == 0:
                raise osv.except_osv('Cuidado!',
                                     u"No Hay mas vacantes en este curso!")

    def confirm_curso(self, cr, uid, ids, context=None):
        register_pool = self.pool.get('curso.registration')
        if self.curso.email_confirmation_id:
            # send reminder that will confirm the curso for all
            # the people that were already confirmed
            reg_ids = register_pool.search(cr, uid, [
                ('curso_id', '=', self.curso.id),
                ('state', 'not in', ['draft', 'cancel'])], context=context)
        # register_pool.mail_user_confirm(cr, uid, reg_ids)
        return self.write(cr, uid, ids, {'state': 'confirm'}, context=context)

    def button_confirm(self, cr, uid, ids, context=None):
        """ Confirmar curso and send confirmation email to all register peoples
        """
        # Verificar si tiene fecha de inicio.
        for curso in self.browse(cr, uid, ids, context=context):
            # chequear si tiene fecha de inicio
            if not (curso.date_begin):
                raise osv.except_osv(('Error!'), (
                    u"No se puede confirmar el curso porque no tiene fecha de inicio."))

            # chequear si tiene agenda
            register_pool = self.pool.get('curso.diary')
            regs_id = register_pool.search(cr, uid,
                                           [('curso_id', '=', curso.id)],
                                           context=context)
            if not regs_id:
                raise osv.except_osv('Error!', (
                    u"No se puede confirmar el curso porque no tiene agenda creada."))

            # chequear si el dia de la semana de la fecha de inicio coincide con la agenda
            for reg in register_pool.browse(cr, uid, regs_id, context=context):
                dt = datetime.strptime(curso.date_begin, "%Y-%m-%d")
                break

            print '>>>>>>>>>> date_begin', dt.strftime('%w'), 'weekday', reg.weekday
            if dt.strftime('%w') != reg.weekday:
                raise osv.except_osv('Error!', (
                    u'El dia de la semana definido por la fecha de inicio no coincide\
                    con el primer dia de la agenda.'))

        if isinstance(ids, (int, long)):
            ids = [ids]
        self.check_registration_limits(cr, uid, ids, context=context)
        return self.confirm_curso(cr, uid, ids, context=context)

    def _get_register(self, cr, uid, ids, fields, args, context=None):
        """ Get Confirm or uncofirm register value.
        @param ids: List of curso registration type's id
        @param fields: List of function fields(register_current and register_prospect).
        @param context: A standard dictionary for contextual values
        @return: Dictionary of function fields value.
        """
        res = {}
        for curso in self.browse(cr, uid, ids, context=context):
            res[curso.id] = {}
            reg_open = reg_done = reg_draft = 0
            for registration in curso.registration_ids:
                if registration.state == 'confirm':
                    reg_open += registration.nb_register
                elif registration.state == 'done':
                    reg_done += registration.nb_register
                elif registration.state == 'draft':
                    reg_draft += registration.nb_register
            for field in fields:
                number = 0
                if field == 'register_current':
                    number = reg_open
                elif field == 'register_attended':
                    number = reg_done
                elif field == 'register_prospect':
                    number = reg_draft
                elif field == 'register_avail':
                    # the number of ticket is unlimited if the curso.register_max
                    # field is not set.
                    # In that cas we arbitrary set it to 9999, it is used in the
                    # kanban view to special case the display of the 'subscribe' button
                    number = curso.register_max - reg_open if curso.register_max != 0 else 9999
                res[curso.id][field] = number
        return res

    def _subscribe_fnc(self, cr, uid, ids, fields, args, context=None):
        """
        This functional fields compute if the current user (uid) is already
        subscribed or not to the curso passed in parameter (ids)
        """
        register_pool = self.pool.get('curso.registration')
        res = {}
        for curso in self.browse(cr, uid, ids, context=context):
            res[curso.id] = False
            curr_reg_id = register_pool.search(cr, uid, [('user_id', '=', uid),
                                                         ('curso_id', '=', curso.id)])
            if curr_reg_id:
                for reg in register_pool.browse(cr, uid, curr_reg_id, context=context):
                    if reg.state in ('confirm', 'done'):
                        res[curso.id] = True
                        continue
        return res

    def get_holiday_dates(self, cr, uid, ids, context=None):
        hd = []
        holidays = self.pool.get('curso.holiday')
        reg_ids = holidays.search(cr, uid, [], context=context)
        for holiday in holidays.browse(cr, uid, reg_ids, context=context):
            hd.append(datetime.strptime(holiday.date, '%Y-%m-%d'))
        return hd

    def _get_day(self, cursor, user_id, context=None):
        return (
            ('0', u'Lunes'),
            ('1', u'Martes'),
            ('2', u'Miércoles'),
            ('3', u'Jueves'),
            ('4', u'Viernes'),
            ('5', u'Sábado'),
            ('6', u'Domingo'))

    def compute_lecture_data(self, cr, uid, ids, date_begin, weekload, tot_lectures,
                             context=None):

        date = datetime.strptime(date_begin, '%Y-%m-%d')
        weekdays = self.weekdays(weekload, date)
        lecture_data = []
        holliday_dates = self.get_holiday_dates(cr, uid, ids, context=None)
        while (len(lecture_data) < tot_lectures):
            if (date in holliday_dates):
                date = date + timedelta(days=weekdays.next_delta())
            else:
                aa = weekdays.current_weekload()
                lecture_data.append({
                    'date': date,
                    'schedule': aa.get('schedule'),
                    'weekday': aa.get('weekday')
                })
                date = date + timedelta(days=weekdays.next_delta())
        return lecture_data

    def create_lectures(self, cr, uid, ids, lecture_data, default_code, context=None):
        lectures_pool = self.pool.get('curso.lecture')
        for reg in self.browse(cr, uid, ids, context=context):
            curso_id = reg.id
        for data in lecture_data:
            lectures_pool.create(cr, uid, {
                'date': data.get('date'),
                'schedule_id': data.get('schedule'),
                'curso_id': curso_id
            })

    def generate_lectures(self, cr, uid, ids, context=None):
        """ Generar las clases que correspondan a este curso
        """
        for reg in self.browse(cr, uid, ids, context=context):
            date_begin = reg.date_begin
            tot_hs_lecture = reg.product.tot_hs_lecture
            hs_lecture = reg.product.hs_lecture
            schedule_1 = reg.schedule_1.id
            weekday_1 = reg.weekday_1
            schedule_2 = reg.schedule_2.id
            weekday_2 = reg.weekday_2
            default_code = reg.default_code

        if (operator.mod(tot_hs_lecture, hs_lecture) != 0):
            raise osv.except_osv(('Error!'), (
                u"la cantidad de horas catedra no es divisible por las horas de clase!."))

        tot_lectures = tot_hs_lecture // hs_lecture
        weekload = []

        if (schedule_1 != False) and (weekday_1 != False):
            weekload = [
                {'schedule': schedule_1,
                 'weekday': weekday_1},
            ]

        if (schedule_2 != False) and (weekday_2 != False):
            weekload.append(
                {'schedule': schedule_2,
                 'weekday': weekday_2}
            )

        if (weekload == []):
            raise osv.except_osv(('Error!'), (u"No se definieron horarios!."))

        lecture_data = self.compute_lecture_data(cr, uid, ids, date_begin, weekload,
                                                 tot_lectures, context=None)
        self.create_lectures(cr, uid, ids, lecture_data, default_code, context=None)
        return 0

    def _get_name(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for curso in self.browse(cr, uid, ids, context=context):
            try:
                init = datetime.strptime(curso.date_begin, "%Y-%m-%d")
            except:
                weekday = day_n = month_n = year_n = '?'
            else:
                lang = self.pool.get('res.users').browse(cr, uid, uid).lang
                lang = 'es_AR'
                weekday = babel.dates.format_datetime(init, format='EEE', locale=lang)
                day_n = init.strftime('%d')
                month_n = init.strftime('%m')
                year_n = init.strftime('%y')
            try:
                ss = curso.schedule_1.start_time
                ee = curso.schedule_1.end_time
                mms = ss - int(ss)
                hhs = int(ss - mms)
                mms = int(mms * 60)
                mme = ee - int(ee)
                hhe = int(ee - mme)
                mme = int(mme * 60)
            except:
                hhs = mms = hhe = mme = 0

            # https://docs.python.org/2/library/datetime.html#datetime-objects
            name = u'[{}] {} {}/{}/{} ({:0>2d}:{:0>2d} {:0>2d}:{:0>2d}) - {}'.format(
                format_instance(curso.product.default_code, curso.instance),
                # Codigo de producto, Nro de instancia
                weekday.capitalize(),  # dia de la semana en letras
                day_n, month_n, year_n,  # dia , mes, anio en numeros
                hhs, mms, hhe, mme,  # hora de inicio hora de fin
                curso.product.name)  # nombre del producto
            res[curso.id] = name
        return res

    def onchange_curso_product(self, cr, uid, ids, product, context=None):
        values = {}
        if product:
            type_info = self.pool.get('product.product').browse(cr, uid, product, context)

            r_pool = self.pool.get('curso.curso')
            records = r_pool.search(cr, uid,
                                    [('default_code', '=', type_info.default_code)],
                                    context=context)

            instance = 0
            for item in r_pool.browse(cr, uid, records, context):
                if item:
                    if (instance < item.instance):
                        instance = item.instance

            instance = instance + 1
            values.update({
                'instance': instance,
            })
        return {'value': values}

    def _get_no_lectures(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for curso in self.browse(cr, uid, ids, context=context):
            try:
                res[curso.id] = curso.tot_hs_lecture / curso.hs_lecture
                if curso.tot_hs_lecture % curso.hs_lecture != 0:
                    raise
            except:
                res[curso.id] = 'Error!'
        return res

    def _get_instance(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for curso in self.browse(cr, uid, ids, context=context):
            res[curso.id] = format_instance(curso.default_code, curso.instance)
        return res

    def _get_next(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for curso in self.browse(cr, uid, ids, context=context):
            res[curso.id] = True

            # me traigo los que estan en borrador de prepo porque no tienen fecha
            res[curso.id] = True
            if curso.state <> 'draft':
                if curso.date_begin < str(date.today()):
                    res[curso.id] = False

        return res

    # curso model
    _columns = {
        'instance': fields.integer('Instancia',
                                   readonly=True,
                                   states={'draft': [('readonly', False)]}),
        'user_id': fields.many2one('res.users', 'Responsable',
                                   readonly=True, states={'done': [('readonly', True)]}),
        'product': fields.many2one('product.product', 'Producto', required=True,
                                   domain="[('tot_hs_lecture','!=','0')]",
                                   readonly=True,
                                   states={'draft': [('readonly', False)]}),
        'register_max': fields.integer('Vacantes max',
                                       help=u"La cantidd máxima de vacantes del curso. \
                                       Si la cantidad de inscripciones es mayor, no se \
                                       puede arrancar el curso. \
                                       (poner 0 para ignorar la regla)",
                                       readonly=True,
                                       states={'draft': [('readonly', False)]}),
        'register_min': fields.integer('Vacantes min', readonly=True,
                                       help=u"La cantidad mínima de inscripciones en el \
                                       curso. Si no hay suficientes inscripcones no se \
                                       puede arrancar el curso. \
                                       (poner 0 para ignorar la regla)",
                                       states={'draft': [('readonly', False)]}),
        'registration_ids': fields.one2many('curso.registration', 'curso_id',
                                            'Inscripciones',
                                            readonly=False,
                                            states={'done': [('readonly', True)],
                                                    'cancel': [('readonly', True)]}),
        'lecture_ids': fields.one2many('curso.lecture', 'curso_id', 'Clases',
                                       readonly=False),
        'date_begin': fields.date('Inicio', required=False,
                                  help=u"La fecha en la que inicia el curso, se puede \
                                  dejar en blanco si no está definida todavia pero se \
                                  debe ingresar para confirmar el curso",
                                  readonly=True, states={'draft': [('readonly', False)]}),

        ###
        'schedule_1': fields.many2one('curso.schedule', 'Horario 1',
                                      readonly=True,
                                      states={'draft': [('readonly', False)]}),
        'schedule_2': fields.many2one('curso.schedule', 'Horario 2',
                                      readonly=True,
                                      states={'draft': [('readonly', False)]}),
        'weekday_1': fields.selection(_get_day, 'Dia 1',
                                      readonly=True,
                                      states={'draft': [('readonly', False)]}),
        'weekday_2': fields.selection(_get_day, 'Dia 2',
                                      readonly=True,
                                      states={'draft': [('readonly', False)]}),
        ###

        'diary': fields.one2many('curso.diary', 'curso_id',
                                 'Agenda',
                                 readonly=True,
                                 states={'draft': [('readonly', False)]}),
        'state': fields.selection([
            ('draft', 'Borrador'),
            ('cancel', 'Cancelado'),
            ('confirm', 'Cursando'),
            ('done', 'Terminado')],
            'Status', readonly=True, required=True,
            track_visibility='onchange',
            help=u'Cuando se crea el curso el estado es \'Borrador\'. Si se confirma el \
                curso el estado es \'Cursando\'. Si el curso termina el estado \
                es \'Terminado\'. Si el curso es cancelado el estado pasa a \'Cancelado\'.'),
        'email_registration_id': fields.many2one('email.template',
                                                 'Confirmación de inscripción',
                                                 help=u'Si definís una plantilla, la \
                                                     misma se enviará cada vez que se \
                                                     confirme una inscripción a este curso.'),
        'email_confirmation_id': fields.many2one('email.template', 'Confirmación curso',
                                                 help=u"Si definis una plantilla de mail, \
                                                     cada participante recibirá este mail \
                                                     anunciando la confirmación del curso."),
        'reply_to': fields.char('Mail de respuesta', size=64, readonly=False,
                                states={'done': [('readonly', True)]},
                                help=u"La dirección de mail del que organiza los cursos, \
                                    cuando el alumno responde el mail que se le envia en \
                                    automático responderá a esta dirección."),
        'main_speaker_id': fields.many2one('res.partner', 'Profesora', readonly=False,
                                           states={'done': [('readonly', True)]},
                                           help=u"La profesora que va a dar el curso."),
        'country_id': fields.related('address_id', 'country_id', type='many2one',
                                     relation='res.country',
                                     string='Country',
                                     readonly=False,
                                     states={'done': [('readonly', True)]}),
        'note': fields.text('Description',
                            readonly=False, states={'done': [('readonly', True)]}),
        'company_id': fields.many2one('res.company', 'Company', required=False,
                                      change_default=True,
                                      readonly=False,
                                      states={'done': [('readonly', True)]}),
        'is_subscribed': fields.function(_subscribe_fnc, type="boolean",
                                         string='Subscribed'),

        # Calculated fields
        'next': fields.function(_get_next, fnct_search=None,
                                string='Curso por venir', method=True,
                                store=True, type='boolean'),
        'curso_instance': fields.function(_get_instance, fnct_search=None,
                                          string='Instancia del curso', method=True,
                                          store=False, type='char'),
        'name': fields.function(_get_name, fnct_search=None, string='Nombre del curso',
                                method=True, store=True,
                                type='char'),
        'no_lectures': fields.function(_get_no_lectures, string='Clases', method=True,
                                       type='char',
                                       help=u"La cantidad de clases que tiene el curso"),
        'register_current': fields.function(_get_register, string='Alumnas',
                                            help=u"La cantidad de alumnas que \
                                                confirmaron pagando (al menos una seña)",
                                            multi='register_numbers'),
        'register_avail': fields.function(_get_register, string='Vacantes',
                                          multi='register_numbers', type='integer'),
        'register_prospect': fields.function(_get_register, string='Interesadas',
                                             help=u"La cantidad de alumnas interesadas \
                                                 que todavía no concretaron",
                                             multi='register_numbers'),
        'register_attended': fields.function(_get_register, string='Egresadas',
                                             multi='register_numbers',
                                             help=u"Cantidad de alumnas que termino el \
                                                 curso con exito."),

        # Related fields
        'tot_hs_lecture': fields.related('product', 'tot_hs_lecture', type='float',
                                         string='Tot Hs', readonly=True),
        'list_price': fields.related('product', 'list_price', type='float',
                                     string='Cuota', readonly=True),
        'hs_lecture': fields.related('product', 'hs_lecture', type='float', string='Hs',
                                     readonly=True),
        'default_code': fields.related('product', 'default_code', type='char',
                                       string=u'Código', readonly=True),
        'no_quotes': fields.related('product', 'no_quotes', type='integer',
                                    string='#cuotas', readonly=True),

        # Deprecated fields
        'type': fields.many2one('curso.type', 'Type of curso', readonly=False,
                                states={'done': [('readonly', True)]}),
    }
    _defaults = {
        'state': 'draft',
        'company_id': lambda self, cr, uid, c: self.pool.get(
            'res.company')._company_default_get(cr, uid, 'curso.curso',
                                                context=c),
        'user_id': lambda obj, cr, uid, context: uid,
    }


def subscribe_to_curso(self, cr, uid, ids, context=None):
    register_pool = self.pool.get('curso.registration')
    user_pool = self.pool.get('res.users')
    num_of_seats = int(context.get('ticket', 1))
    self.check_registration_limits_before(cr, uid, ids, num_of_seats, context=context)
    user = user_pool.browse(cr, uid, uid, context=context)
    curr_reg_ids = register_pool.search(cr, uid, [('user_id', '=', user.id),
                                                  ('curso_id', '=', ids[0])])
    # the subscription is done with SUPERUSER_ID because in case we share the
    # kanban view, we want anyone to be able to subscribe
    if not curr_reg_ids:
        curr_reg_ids = [register_pool.create(cr, SUPERUSER_ID,
                                             {'curso_id': ids[0], 'email': user.email,
                                              'name': user.name,
                                              'user_id': user.id,
                                              'nb_register': num_of_seats})]
    else:
        register_pool.write(cr, uid, curr_reg_ids, {'nb_register': num_of_seats},
                            context=context)
    return register_pool.confirm_registration(cr, SUPERUSER_ID, curr_reg_ids,
                                              context=context)


def unsubscribe_to_curso(self, cr, uid, ids, context=None):
    register_pool = self.pool.get('curso.registration')
    # the unsubscription is done with SUPERUSER_ID because in case we share the
    # kanban view, we want anyone to be able to unsubscribe
    curr_reg_ids = register_pool.search(cr, SUPERUSER_ID, [('user_id', '=', uid),
                                                           ('curso_id', '=', ids[0])])
    return register_pool.button_reg_cancel(cr, SUPERUSER_ID, curr_reg_ids,
                                           context=context)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
