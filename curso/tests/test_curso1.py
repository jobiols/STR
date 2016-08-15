# -*- coding: utf-8 -*-
#####################################################################################
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
#####################################################################################
from openerp.tests.common import SingleTransactionCase

# testear con
# ./odooenv.py -Q cursos test_curso1.py -c makeover -d makeover_test -m curso
#

class TestCurso(SingleTransactionCase):

    def setUp(self):
        super(TestCurso, self).setUp()
        print 'test curso setup ---------------------------------------------------------'
        # creo todos los objetos
        self.partner_obj = self.env['res.partner']
        self.product_obj = self.env['product.product']
        self.curso_obj = self.env['curso.curso']
        self.diary_obj = self.env['curso.diary']
        self.schedule_obj = self.env['curso.schedule']
        self.registration_obj = self.env['curso.registration']

        # creo un alumno
        self.partner = self.partner_obj.create({
            'name': 'Juana Perez Alumna'})

    def test_CreateSchedules_01(self):
        print 'test curso create schedules ----------------------------------'
        # creo tres horarios
        self.schedule1 = self.schedule_obj.create({
            'start_time':12.5,
            'end_time':15.5
        })
        self.schedule2 = self.schedule_obj.create({
            'start_time':11,
            'end_time':16
        })
        self.schedule3 = self.schedule_obj.create({
            'start_time':4,
            'end_time':6
        })

        print 'test schedules'
        self.assertEqual(self.schedule1.name,u'12:30 - 15:30 (3hs)','El nombre está mal')
        self.assertEqual(self.schedule2.name,u'11:00 - 16:00 (5hs)','El nombre está mal')
        self.assertEqual(self.schedule3.name,u'04:00 - 06:00 (2hs)','El nombre está mal')

        # creo un producto con tres clases
        print 'create product'
        self.product = self.product_obj.create({
            'tot_hs_lecture': 15,
            'hs_lecture': 5,
            'no_quotes': 10,
            'default_code': 'SPR',
            'list_price': 800,
            'type': 'service',
            'name': 'Curso de maquillaje Social Profesional rafañuso',
            'agenda': 'Titulo Cuerpo del texto **negrita** Año 2016',
            'description': 'este es un curso **de prueba** para el test en UTF8 ajá tomá ñoño'
        })

        # creo una plantilla de clases para este producto
        self.ids = [self.product.id]
        self.product.button_generate_lecture_templates()

        # creo un curso basado en este producto
        self.curso1 = self.curso_obj.create({
            'product':self.product.id,
        })

        # chequeo state instance y name
        self.assertEqual(self.curso1.state,'draft','El estado debe ser draft')
        self.assertEqual(self.curso1.name,
                         u'[SPR/00] ? ?/?/? (00:00 00:00) - Curso de maquillaje Social Profesional rafañuso',
                         'El nombre está mal')

        # creo otro curso basado en este producto
        self.curso2 = self.curso_obj.create({
            'product':self.product.id
        })

        # chequeo state instance y name
        self.assertEqual(self.curso1.state,'draft','El estado debe ser draft')
        self.assertEqual(self.curso1.name,
                         u'[SPR/00] ? ?/?/? (00:00 00:00) - Curso de maquillaje Social Profesional rafañuso',
                         'El nombre está mal')

        # creo un diario con tres dias agregandolo al curso 2, 3 clases en la semana
        self.diary = self.diary_obj.create({
            'curso_id': self.curso2.id,
            'weekday': '1',
            'seq': 1,
            'schedule': self.schedule1.id
        })
        self.diary = self.diary_obj.create({
            'curso_id': self.curso2.id,
            'weekday': '2',
            'seq': 2,
            'schedule': self.schedule2.id
        })
        self.diary = self.diary_obj.create({
            'curso_id': self.curso2.id,
            'weekday': '3',
            'seq': 3,
            'schedule': self.schedule3.id
        })

        # le agrego la fecha al curso 2
        self.curso2.date_begin = '2016-01-11'


        # registro la alumna en el curso 2
        vals = {
            'curso_id': self.curso2.id,
            'partner_id': self.partner.id,
            'user_id': 1
        }
        self.registration_1 = self.registration_obj.create(vals)


        # chequeando generacion de plantillas
        ##################################################################################
        self.assertEqual(self.schedule1.formatted_start_time,u'12:30',
                         'Falla formatted_start_time')
        self.assertEqual(self.registration_1.get_formatted_begin_date(),u'Lunes 11/01/2016',
                         'Falla get_formatted_begin_date')
        self.assertEqual(self.registration_1.get_formatted_begin_time(),u'12:30',
                         'Falla get_formatted_begin_time')






# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: