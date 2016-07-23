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
from datetime import datetime, timedelta, date
import operator
from openerp import api

from openerp.osv import fields, osv
from openerp import SUPERUSER_ID
import locale

try:
    locale.setlocale(locale.LC_ALL, 'es_AR.utf8')
except:
    a = 1

class curso_information(osv.osv_memory):
    """ Wizard para generar documentacion de los cursos
    """
    _name = 'curso.information'
    _description = __doc__

    def button_information(self, cr, uid, ids, context=None):
        curso_pool = self.pool.get('curso.curso')
        for curso in curso_pool.browse(cr, uid, context['active_ids'], context):
            curso.button_generate_doc_curso()
        return True


class curso_curso(osv.osv):
    """ Representa una instancia de un curso """
    _name = 'curso.curso'
    _description = __doc__
    _order = 'date_begin'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    class weekdays():
        _weekload = []
        _ix = 0

        def __init__(self, wl, date):
            #            print 'weekday constructor ---------------------------------------------------'
            # ordering the weekload by weekday
            wl.sort(key=lambda b: b['weekday'])

            #            for a in wl: print a
            #            print 'start date', date

            self._weekload = wl
            self._start_date = self._current_date = date

            # adjust ix to point the right weekday
            start_weekday = int(self._start_date.strftime('%w'))
            for ix in range(len(wl)):
                #                print ix, start_weekday, wl[ix]['weekday']
                if start_weekday == wl[ix]['weekday']:
                    self._ix = ix

        def get_date(self):
            return self._current_date

        def get_schedule(self):
            return self._weekload[self._ix]['schedule']

        def get_room(self):
            return 'A'

        def _gwd(self, ix):
            return self._weekload[ix]['weekday']

        def next_class(self):

            # move ix one ahead
            ix_1 = self._ix
            self._ix += 1
            if self._ix >= len(self._weekload):
                self._ix = 0
            ix = self._ix

            # calculate current date
            if self._gwd(ix) > self._gwd(ix_1):
                self._current_date += timedelta(days=self._gwd(ix) - self._gwd(ix_1))
            else:
                self._current_date += timedelta(
                    days=7 - (self._gwd(ix_1) - self._gwd(ix)))

    def get_formatted_instance(self, cr, uid, curso_id, context=None):
        for curso in self.browse(cr, uid, curso_id, context=context):
            return '{}/{:0>2d}'.format(curso.default_code, curso.instance)
        return False

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
            if clase['name']:
                dd = clase['name']
            else:
                dd = "no hay tema"
            ret += "			<td>" + dd + "</td>"
            ret += "		</tr>"
        ret += "</tbody>"
        ret += "</table>"

        return ret

    def button_generate_doc_curso(self, cr, uid, ids, context=None):
        """
        Genera planilla de asistencia para el curso
        """
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
            records = lect_pool.search(
                cr, uid, [('curso_id', '=', curso.id)], order="date")
            for lect in lect_pool.browse(cr, uid, records, context=context):
                # TODO   chequear esto!!!
                d = {
                    'fecha': datetime.strptime(
                        lect.date, "%Y-%m-%d").strftime("%d/%m/%y"),
                    'name': lect.name,
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
        return super(curso_curso, self).copy(
            cr, uid, id, default=default, context=context)

    def check_registration_limits(self, cr, uid, ids, context=None):
        for self.curso in self.browse(cr, uid, ids, context=context):
            total_confirmed = self.curso.register_current
            if total_confirmed < self.curso.register_min or \
                                    total_confirmed > self.curso.register_max and \
                                    self.curso.register_max != 0:
                raise osv.except_osv('Error!',
                    u"El total de inscripciones confirmadas para el curso '%s' no \
                    cumple con los requerimientos esperados de minimo/maximo. \
                    Reconsidere estos limites antes de continuar." % (
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

    def get_weekload(self, cr, uid, ids, context=None):
        ret = []
        for curso in self.browse(cr, uid, ids, context=context):
            diary_obj = self.pool.get('curso.diary')
            diary_ids = diary_obj.search(
                cr, uid, [('curso_id', '=', curso.id)], context=context)
            for day in diary_obj.browse(cr, uid, diary_ids):
                ret.append({
                    'weekday': int(day.weekday),
                    'schedule': day.schedule
                })

        return ret

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

    # Estados de los cursos
    ###############################################################################

    def button_curso_confirm(self, cr, uid, ids, context=None):
        """ Confirmar curso chequeando antes que tenga fecha de inicio y que coincida con la agenda
        """
        # Verificar si tiene fecha de inicio.
        for curso in self.browse(cr, uid, ids, context=context):
            # chequear si tiene fecha de inicio
            if not (curso.date_begin):
                raise osv.except_osv(('Error!'), (
                    u"No se puede confirmar el curso porque no tiene fecha de inicio."))

            # chequear si tiene agenda
            diary_obj = self.pool.get('curso.diary')
            diary_ids = diary_obj.search(
                cr, uid, [('curso_id', '=', curso.id)], context=context)
            if not diary_ids:
                raise osv.except_osv(
                    'Error!',
                    u"No se puede confirmar el curso porque no tiene agenda creada.")

            # chequear si el dia de inicio corresponde a la agenda
            for diary_line in diary_obj.browse(cr, uid, diary_ids, context=context):
                if not diary_line.check_weekday(curso.date_begin):
                    raise osv.except_osv(
                        'Error!',
                        u'No se puede confirmar el curso porque la fecha de inicio (%s) cae en un dia \
                        que no es el primer dia de la agenda (%s).' % (
                            curso.date_begin, diary_line.weekday_name))

                if isinstance(ids, (int, long)):
                    ids = [ids]
                self.check_registration_limits(cr, uid, ids, context=context)
                return self.confirm_curso(cr, uid, ids, context=context)

    def button_curso_done(self, cr, uid, ids, context=None):
        """
        Terminar el curso
        """
        # si existe al menos una en estado signed no se puede terminar el curso
        # si existe al menos una en estado confirm no se puede terminar el curso
        reg_obj = self.pool.get('curso.registration')
        reg_ids = reg_obj.search(cr, uid,
                                 [('curso_id', 'in', ids),
                                  '|',
                                  ('state', '=', 'signed'),
                                  ('state', '=', 'confirm')
                                  ], context=context)
        if reg_ids:
            raise osv.except_osv(
                'Error!',
                u"Para terminar el curso las alumnas deben estar en estado \
                cumplido, o cancelado.")

        # si existen interesadas hay que proponer moverlas a otro curso
        for curso_reg in reg_obj.browse(cr, uid, reg_ids, context=context):
            if not (
                            (curso_reg.state == 'done') or
                            (curso_reg.state == 'cancel') or
                        (curso_reg.state == 'draft')
            ):
                raise osv.except_osv(
                    'Error!',
                    u"Para terminar el curso las alumnas deben estar en estado cumplido, \
                    cancelado o interesada. Usá el menú Mover / Copiar para pasarlas a otro \
                    curso")

        return self.write(cr, uid, ids, {'state': 'done'}, context=context)

    def button_curso_draft(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'draft'}, context=context)

    def button_curso_cancel(self, cr, uid, ids, context=None):
        """
        Canelar el curso
        """
        # si existe al menos una en estado signed no se puede cancelar el curso
        # si existe al menos una en estado confirm no se puede cancelar el curso
        # si existe al menos una en estado cumplido no se puede cancelar el curso
        # si existen interesadas hay que proponer moverlas a otro curso

        # chequear que todas las alumnas estan canceladas
        reg_obj = self.pool.get('curso.registration')
        reg_ids = reg_obj.search(cr, uid, [('curso_id', 'in', ids)], context=context)
        for curso_reg in reg_obj.browse(cr, uid, reg_ids, context=context):
            if not (curso_reg.state == 'cancel'):
                raise osv.except_osv(
                    'Error!',
                    u'Para cancelar el curso todas las alumnas deben estar en estado Cancelado. \
                      Podes usar el menú Mover / Copiar para pasarlas a otro curso')

        # borrar todas las clases
        lecture_obj = self.pool['curso.lecture']
        class_ids = lecture_obj.search(cr,uid,[('curso_id','=',ids)])
        lecture_obj.unlink(cr,uid,class_ids)

        return self.write(cr, uid, ids, {'state': 'cancel'}, context=context)

    def get_holiday_dates(self, cr, uid, ids, context=None):
        hd = []
        holidays = self.pool.get('curso.holiday')
        reg_ids = holidays.search(cr, uid, [], context=context)
        for holiday in holidays.browse(cr, uid, reg_ids, context=context):
            hd.append(datetime.strptime(holiday.date, '%Y-%m-%d'))
        return hd

    def lectures_list(self, weekdays, no_lectures):
        #        print 'lectures_list >>>>>>>>>>>>>>>>>>>>>>>>>>>>>', no_lectures

        ret = []
        for ix in range(no_lectures):
            ret.append((
                weekdays.get_date(),
                weekdays.get_schedule(),
                weekdays.get_room()))
            weekdays.next_class()

        #        print '------------------------------------------------------------------'
        #        for date, schedule, room in ret:
        #            print date, schedule.name, room
        #        print '------------------------------------------------------------------'
        return ret

    def lecture_overlaps(self, date, schedule, room):
        return False

    @api.v7
    def get_lecture_templates(self, cr, uid, ids, product_id, context=None):
        template_obj = self.pool['curso.lecture_template']
        ids = template_obj.search(
            cr, uid, [('product_id', '=', product_id)], context=context)
        ret = []
        ii = 0
        for rec in template_obj.browse(cr, uid, ids):
            ret.append({'name': rec.text})

        return ret

    @api.v8
    def get_lecture_templates(self, product_id):
        template_obj = self.env['curso.lecture_template']

        ret = []
        for rec in template_obj.search([('product_id', '=', product_id)]):
            ret.append({'name': rec.text})

        return ret

    def button_generate_lectures(self, cr, uid, ids, context=None):
        """ Generar las clases que correspondan a este curso
        """
        for curso in self.browse(cr, uid, ids, context=context):
            date_begin = datetime.strptime(curso.date_begin, '%Y-%m-%d')
            tot_hs_lecture = curso.tot_hs_lecture
            hs_lecture = curso.hs_lecture
            default_code = curso.default_code
            if (operator.mod(tot_hs_lecture, hs_lecture) != 0):
                raise osv.except_osv(
                    'Error!',
                    u"la cantidad de horas catedra no es divisible por las horas de clase!.")

            no_lectures = int(tot_hs_lecture // hs_lecture)
            weekload = self.get_weekload(cr, uid, ids)

            if (weekload == []):
                raise osv.except_osv('Error!', u"No se definió la agenda!.")

            # get lecture templates
            lecture_templates = self.get_lecture_templates(
                cr, uid, ids, curso.product.id, context=context)

            # get a lectures list or an exception if overlaps.
            lectures = []
            for date, schedule, room in self.lectures_list(
                    self.weekdays(weekload, date_begin), no_lectures):
                if not self.lecture_overlaps(date, schedule, room):
                    lectures.append(
                        {'date': date,
                         'schedule': schedule,
#                         'room': room,
                         'curso': curso})
                else:
                    raise osv.except_osv(
                        'Error!',
                        u'La clase del %s en el horario %s y en el aula %s se superpone con una ya existente',
                        date, schedule.name, room)

            if len(lectures) != len(lecture_templates):
                raise osv.except_osv(
                    'Error!',
                    u'La cantidad de clases no coincide con la cantidad de contenidos.')

            lecs = []
            for ix, lec in enumerate(lectures):
                lec['date'] = lectures[ix]['date']
                lec['name'] = lecture_templates[ix]['name']
                lec['curso_id'] = lectures[ix]['curso'].id
                lec['schedule_id'] = lectures[ix]['schedule'].id
                lec['date_start'] = lectures[ix]['schedule'].start_datetime(lec['date'])
                lec['date_stop'] = lectures[ix]['schedule'].stop_datetime(lec['date'])
                lecs.append(lec)

            # Add lectures
            lectures_pool = self.pool.get('curso.lecture')
            ids = lectures_pool.search(cr, uid, [('curso_id', '=', curso.id)])
            lectures_pool.unlink(cr, uid, ids)
            for lec in lecs:
                lectures_pool.create(cr, uid, lec)

    def _check_change_begin_date(self, cr, uid, ids, context=None):
        for curso in self.browse(cr, uid, ids, context=context):
            diary_pool = self.pool['curso.diary']
            ids = diary_pool.search(
                cr, uid, [('curso_id', '=', curso.id)], context=context)
            for diary_line in diary_pool.browse(cr, uid, ids, context):
                diary_weekday = diary_line.weekday
                weekday = datetime.strptime(curso.date_begin, '%Y-%m-%d').strftime('%w')
                if weekday != diary_weekday:
                    raise osv.except_osv('Error!', (
                        u"La fecha de inicio no corresponde con el primer dia de la agenda"))
                return True
        return True

    def onchange_diary_ids(self, cr, uid, ids, context=None):
        self._check_change_begin_date(cr, uid, ids, context=context)
        return True

    def onchange_date_begin(self, cr, uid, ids, context=None):
        self._check_change_begin_date(cr, uid, ids, context=context)
        return self.pool

    def onchange_curso_product(self, cr, uid, ids, product, context=None):
        values = {}
        if product:
            type_info = self.pool.get('product.product').browse(cr, uid, product, context)

            r_pool = self.pool.get('curso.curso')
            records = r_pool.search(
                cr, uid, [('default_code', '=', type_info.default_code)],
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

    def clone_diary(self, cr, uid, ids, curso_from, curso_to, context=None):
        diary_obj = self.pool['curso.diary']
        ids = diary_obj.search(cr, uid, [('curso_id', '=', curso_from)])
        for diary in diary_obj.browse(cr, uid, ids, context=context):
            #            print diary.id
            diary_obj.create(cr, uid, {
                'curso_id': curso_to,
                'weekday': diary.weekday,
                'schedule': diary.schedule.id,
                'seq': diary.seq
            })

    def button_update_child_from_parent(
            self, cr, uid, ids, parent_id, class_id, context=None):
        """
        Update child with parent information
            date_begin: the date of the lecture the child is inserted on
            diary_id: create the same diary as parent
            child: True
        """
        #        print 'button_update_child_from_parent ', parent_id, class_id
        res = {}
        for curso in self.browse(cr, uid, ids, context=context):
            #            print curso.name

            self.clone_diary(cr, uid, ids, parent_id, curso.id, context=context)

            lecture_obj = self.pool['curso.lecture']
            ids = lecture_obj.search(cr, uid, [('id', '=', class_id)])
            for lecture in lecture_obj.browse(cr, uid, ids):
                #                print lecture.name
                res['date_begin'] = lecture.date
            #                print res


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
