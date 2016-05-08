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

class TestCurso(SingleTransactionCase):

    def setUp(self):
        super(TestCurso, self).setUp()
        print 'test curso setup --------------------------------------------------------------------'
        # creo todos los objetos
        self.partner_obj = self.env['res.partner']
        self.product_obj = self.env['product.product']
        self.curso_obj = self.env['curso.curso']
        self.diary_obj = self.env['curso.diary']
        self.schedule_obj = self.env['curso.schedule']

        # creo un alumno
        self.partner = self.partner_obj.create({
            'name': 'Juana Perez Alumna'})

    def CreateSchedules_01(self):
        print 'test curso create schedules'
        # creo tres horarios
        self.schedule1 = self.schedule_obj.create({
            'start_time':12,
            'end_time':15
        })
        self.schedule2 = self.schedule_obj.create({
            'start_time':11,
            'end_time':16
        })
        self.schedule3 = self.schedule_obj.create({
            'start_time':4,
            'end_time':6
        })

    def TestSchedules_02(self):
        self.assertEqual(self.schedule1.name,u'12:00 - 15:00 (3hs)','El nombre está mal')
        self.assertEqual(self.schedule2.name,u'11:00 - 16:00 (5hs)','El nombre está mal')
        self.assertEqual(self.schedule3.name,u'04:00 - 06:00 (2hs)','El nombre está mal')

    def CreateProduct_03(self):
        # creo un producto con tres clases
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

    def CreateCurso1_04(self):
        # creo un curso basado en este producto
        self.curso1 = self.curso_obj.create({
            'product':self.product.id
        })

        # chequeo state instance y name
        self.assertEqual(self.curso1.state,'draft','El estado debe ser draft')
        self.assertEqual(self.curso1.instance,1,'La instancia debe ser uno')
        self.assertEqual(self.curso1.name,
                         u'[SPR/01] ? ?/?/? (00:00 00:00) - Curso de maquillaje Social Profesional rafañuso',
                         'El nombre está mal')

    def CreateCurso2_05(self):
        # creo otro curso basado en este producto
        self.curso2 = self.curso_obj.create({
            'product':self.product.id
        })

        # chequeo state instance y name
        self.assertEqual(self.curso1.state,'draft','El estado debe ser draft')
        self.assertEqual(self.curso1.instance,2,'La instancia debe ser uno')
        self.assertEqual(self.curso1.name,
                         u'[SPR/02] ? ?/?/? (00:00 00:00) - Curso de maquillaje Social Profesional rafañuso',
                         'El nombre está mal')

    def CreateDiary_06(self):
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

        # chequeo de nuevo el nombre
        self.assertEqual(self.name,
                         u'[SPR/02] Mon 11/01/16 (12:00 15:00) - Curso de maquillaje Social Profesional rafañuso',
                         'El nombre está mal formado')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: