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
from openerp.tests.common import SingleTransactionCase


class TestCurso(SingleTransactionCase):
    def setUp(self):
        super(TestCurso, self).setUp()

    def test_hijo(self):
        print '= configurando para el test ===================='
        # creo todos los objetos
        self.partner_obj = self.env['res.partner']
        self.product_obj = self.env['product.product']
        self.curso_obj = self.env['curso.curso']
        self.diary_obj = self.env['curso.diary']
        self.schedule_obj = self.env['curso.schedule']

        ############################################################
        #
        # creo un producto curso para el padre
        self.product_1 = self.product_obj.create({
            'tot_hs_lecture': 160,
            'hs_lecture': 4,
            'no_quotes': 10,
            'default_code': 'CFC',
            'list_price': 1200,
            'type': 'service',
            'name': 'Curso de formacion completa 2016',
            'agenda': 'Titulo Cuerpo del texto **negrita** Año 2016',
            'description': 'este es un curso **padre** para el test en UTF8 ajá tomá ñoño'
        })
        # generar plantilla de clases
        self.product_1.button_generate_lecture_templates()

        # generar documentacion
        self.product_1.button_generate_doc()

        # creo el horario
        self.schedule_1 = self.schedule_obj.create({
            'start_time': 12,
            'end_time': 16
        })

        # creamos la instancia del curso padre
        self.curso_1 = self.curso_obj.create({
            'product': self.product_1.id,
            'date_begin': '01/06/2016',
        })

        # creo el diario con el horario
        self.diary = self.diary_obj.create({
            'curso_id': self.curso_1.id,
            'weekday': '3',
            'seq': 1,
            'schedule': self.schedule_1.id
        })

        # creamos las clases del curso padre
        self.curso_1.button_generate_lectures()

        ############################################################
        #
        # creo producto curso para el hijo
        self.product_2 = self.product_obj.create({
            'tot_hs_lecture': 80,
            'hs_lecture': 4,
            'no_quotes': 5,
            'default_code': 'SPR',
            'list_price': 800,
            'type': 'service',
            'name': 'Maquillaje social profesional regular',
            'agenda': 'Titulo Cuerpo del texto **negrita** Año 2016',
            'description': 'este es un curso **hijo** para el test en UTF8 ajá tomá ñoño'
        })

        # generar documentacion
        self.product_2.button_generate_doc()

        # creo el horario
        self.schedule_1 = self.schedule_obj.create({
            'start_time': 12,
            'end_time': 16
        })

        # creamos la instancia del curso hijo
        self.curso_2 = self.curso_obj.create({
            'product': self.product_2.id,
            'child': True,
            'parent_curso_id': self.curso_1.id,
            'first_lecture_id': 1
        })

        print '= configuración lista =========================='

        print '= testeando 1 =================================='
        self.curso_1.button_curso_confirm()
