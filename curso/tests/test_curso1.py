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
from openerp.tests.common import TransactionCase

# testear con
# ./odooenv.py -Q cursos test_curso1.py -c makeover -d makeover_test -m curso
#

class TestCurso(TransactionCase):
    def setUp(self):
        """ Setup for test """

        super(TestCurso, self).setUp()

        # creo todos los objetos
        self.partner_obj = self.env['res.partner']
        self.product_obj = self.env['product.product']
        self.curso_obj = self.env['curso.curso']
        self.diary_obj = self.env['curso.diary']
        self.schedule_obj = self.env['curso.schedule']
        self.registration_obj = self.env['curso.registration']
        self.email_template_obj = self.env['email.template']

        # creo un alumno
        self.partner = self.partner_obj.create({
            'name': 'Juana Perez Alumna'})

        # creo una profesora
        self.partner_prof = self.partner_obj.create({
            'name': 'Juana Perez Profesora'})

    def test_CreateSchedules_01(self):
        """ test curso create schedules """
        print 'test from test_curso1.py --------------------------------'
        # creo tres horarios
        self.schedule1 = self.schedule_obj.create({
            'start_time': 12.5,
            'end_time': 15.5
        })
        self.schedule2 = self.schedule_obj.create({
            'start_time': 11,
            'end_time': 16
        })
        self.schedule3 = self.schedule_obj.create({
            'start_time': 4,
            'end_time': 6
        })

        self.assertEqual(self.schedule1.name, u'12:30 - 15:30 (3hs)',
                         'El nombre está mal')
        self.assertEqual(self.schedule2.name, u'11:00 - 16:00 (5hs)',
                         'El nombre está mal')
        self.assertEqual(self.schedule3.name, u'04:00 - 06:00 (2hs)',
                         'El nombre está mal')

        # creo un producto con tres clases
        self.product = self.product_obj.create({
            'tot_hs_lecture': 15,
            'hs_lecture': 5,
            'no_quotes': 10,
            'default_code': 'SPX',
            'list_price': 800,
            'type': 'curso',
            'name': 'Curso de maquillaje Social Profesional rafañuso',
            'agenda': 'Titulo Cuerpo del texto **negrita** Año 2016',
            'description': 'este es un curso **de prueba** para el test en UTF8 ajá tomá ñoño'
        })

        # creo un template de mail para este producto
        self.email_template_1 = self.email_template_obj.create({
            'name': 'plantilla de mail'
        })

        # creo una plantilla de clases para este producto
        self.ids = [self.product.id]
        self.product.button_generate_lecture_templates()

        # creo un curso basado en este producto
        self.curso1 = self.curso_obj.create({
            'product': self.product.id,
            'main_speaker_id': self.partner_prof.id,
            'email_registration_id': self.email_template_1.id
        })

        # chequeo state instance y name
        self.assertEqual(self.curso1.state, 'draft', 'El estado debe ser draft')
        self.assertEqual(self.curso1.name,
                         u'[SPX/00] ? ?/?/? (00:00 00:00) - Curso de maquillaje Social Profesional rafañuso',
                         'El nombre está mal')

        # creo otro curso basado en este producto
        self.curso2 = self.curso_obj.create({
            'product': self.product.id,
            'main_speaker_id': self.partner_prof.id,
            'email_registration_id': self.email_template_1.id
        })

        # chequeo state instance y name
        self.assertEqual(self.curso1.state, 'draft', 'El estado debe ser draft')
        self.assertEqual(self.curso1.name,
                         u'[SPX/00] ? ?/?/? (00:00 00:00) - Curso de maquillaje Social Profesional rafañuso',
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
        self.assertEqual(self.schedule1.formatted_start_time, u'12:30',
                         'Falla formatted_start_time')
        self.assertEqual(self.registration_1.get_formatted_begin_date()[-10:],
                         u'11/01/2016',
                         'Falla get_formatted_begin_date')
        self.assertEqual(self.registration_1.get_formatted_begin_time(), u'12:30',
                         'Falla get_formatted_begin_time')

        # check formatted dia
        # ry
        data = self.product._get_formatted_diary(self.curso2.id)

        # chequeo titulo del curso para html

    #        data = self.product._get_html_data()
    #        self.assertEqual(data['code'],
    #                         u'SPX',
    #                         'Falla codigo')
    #        self.assertEqual(data['description'],
    #                         u'Curso de maquillaje Social Profesional rafañuso',
    #                         'Falla descripcion')

    #        self.product.get_html_data()


    def test_generate_html_02(self):
        """ Chequea generación de html """
        # creo el producto SPX
        ##################################################################################
        self.product1 = self.product_obj.create({
            'tot_hs_lecture': 80,
            'hs_lecture': 4,
            'no_quotes': 5,
            'default_code': 'SPX',
            'list_price': 1200,
            'type': 'curso',
            'name': 'Maquillaje Social Profesional',
            'agenda':
                """
    - Presentación, protocolo y herramientas de trabajo. / Psicología y marketing del maquillaje.
    - Biotipos y fototipos cutáneos / Cuidados de la piel, vehículo e higiene .
    - Correcciones y puntos de luz / Diferentes texturas de bases de maquillaje 1.
    - Análisis de la morfología del rostro - visagismo en crema.
    - Visagismo en polvo & strobing.
    - Teoría del color apllicada al maquillaje / Esfumatura de ojos juntos y separados (delineado).
    - Esfumatura de ojos poco redondos y chicos (delineado).
    - Esfumatura de ojos hundidos y saltones (delineado).
    - Esfumatura de ojos caídos y encapotados (delineado). / Colocación de pestañas y reconocimiento de adhesivos  Diseño y perfilado de  cejas.
    - Diseño y perfilado de cejas. / Corrector o color? Rubor - labios.
    - Evaluación.
    - Maquillaje para adolescentes / protocolo para evento
    - Maquillaje para novias  / protocolo para evento
    - Maquillaje de rejuvenecimiento  / protocolo para evento
    - Adaptación de maquillajes a las distintas razas y culturas / maquillaje masculino
    - Maquillaje Masculino
    - Maquillaje para pasarela y fantasia. Esfumatura de ojos de moda y cut crease
    - Técnicas para fotografía color, blanco y negro, cinematografía, video, TV en HD / Como hacer cambios rápidos de maquillaje en una sesión de fotos / Shooting
    - Organización de cursos de automaquillaje - autoempleo
    - Evaluación con trabajo práctico final.
                """,
            'description':
                """
    Te formarás con los mejores conocimientos, información, profesionales de trayectoria; en un lugar único, destacando el
    ambiente cálido y humano. Con sólidos contenidos teóricos que fundamentan la carrera dando una base para que luego el
    estudiante pueda canalizar su arte. El estudio de la estructura facial, la teoría del color y las características de
    cada tipo de piel, son algunas de las herramientas que el estudiante podrá obtener.
                """
        })

        # creo el producto QBX
        ##################################################################################
        self.product2 = self.product_obj.create({
            'tot_hs_lecture': 40,
            'hs_lecture': 8,
            'no_quotes': 1,
            'default_code': 'QBX',
            'list_price': 6000,
            'type': 'curso',
            'name': 'Body Art',
            'agenda':
                """
                """,
            'description':
                """
                """
        })

        # creo un curso basado en producto 1
        ##################################################################################
        self.curso1 = self.curso_obj.create({
            'product': self.product1.id,
            'main_speaker_id': self.partner_prof.id,
            'email_registration_id': self.email_template_1.id
        })

        # creo un curso basado en producto 1
        ##################################################################################
        self.curso2 = self.curso_obj.create({
            'product': self.product1.id,
            'main_speaker_id': self.partner_prof.id,
            'email_registration_id': self.email_template_1.id
        })

        # creo un curso basado en producto 2
        ##################################################################################
        self.curso3 = self.curso_obj.create({
            'product': self.product2.id,
            'main_speaker_id': self.partner_prof.id,
            'email_registration_id': self.email_template_1.id
        })

        # creo un curso basado en producto 2
        ##################################################################################
        self.curso4 = self.curso_obj.create({
            'product': self.product2.id,
            'main_speaker_id': self.partner_prof.id,
            'email_registration_id': self.email_template_1.id
        })

        # creo todos los horarios
        ##################################################################################
        self.schedule1 = self.schedule_obj.create({'start_time': 12, 'end_time': 16})
        self.schedule2 = self.schedule_obj.create({'start_time': 15, 'end_time': 19})
        self.schedule3 = self.schedule_obj.create({'start_time': 10, 'end_time': 17})
        self.schedule4 = self.schedule_obj.create({'start_time': 15.5, 'end_time': 17.5})
        self.schedule5 = self.schedule_obj.create({'start_time': 20, 'end_time': 21})
        self.schedule6 = self.schedule_obj.create({'start_time': 12.3, 'end_time': 16.3})

        # creo todos los diarios
        ##################################################################################
        self.diary11 = self.diary_obj.create({
            'curso_id': self.curso1.id, 'weekday': '1', 'seq': 1, 'schedule': self.schedule1.id
        })
        ###
        self.diary21 = self.diary_obj.create({
            'curso_id': self.curso2.id, 'weekday': '2', 'seq': 1, 'schedule': self.schedule2.id
        })
        ###
        self.diary31 = self.diary_obj.create({
            'curso_id': self.curso3.id, 'weekday': '3', 'seq': 1, 'schedule': self.schedule3.id
        })
        self.diary32 = self.diary_obj.create({
            'curso_id': self.curso3.id, 'weekday': '5', 'seq': 2, 'schedule': self.schedule4.id
        })
        self.diary33 = self.diary_obj.create({
            'curso_id': self.curso3.id, 'weekday': '5', 'seq': 3, 'schedule': self.schedule5.id
        })
        ###
        self.diary41 = self.diary_obj.create({
            'curso_id': self.curso4.id, 'weekday': '3', 'seq': 1, 'schedule': self.schedule6.id
        })
        self.diary42 = self.diary_obj.create({
            'curso_id': self.curso4.id, 'weekday': '4', 'seq': 2, 'schedule': self.schedule6.id
        })
        self.diary43 = self.diary_obj.create({
            'curso_id': self.curso4.id, 'weekday': '5', 'seq': 3, 'schedule': self.schedule6.id
        })
        self.diary44 = self.diary_obj.create({
            'curso_id': self.curso4.id, 'weekday': '1', 'seq': 4, 'schedule': self.schedule6.id
        })
        self.diary45 = self.diary_obj.create({
            'curso_id': self.curso4.id, 'weekday': '2', 'seq': 5, 'schedule': self.schedule6.id
        })

        # les agrego la fecha de inicio
        self.curso1.date_begin = '2016-08-01'
        self.curso2.date_begin = '2016-08-09'
        self.curso3.date_begin = '2016-08-17'
        self.curso4.date_begin = '2016-08-31'

        ##################################################################################
        # Se chequea el producto

        data = self.product1.info_curso_html_data(debug=True)
        self.assertEqual(data['name'], u'Maquillaje Social Profesional', 'error 01')

        self.assertEqual(data['comercial_data'][0], u'Matricula bonificada.',
                         'error 02')
        self.assertEqual(data['comercial_data'][1], u'No se cobra derecho de examen.',
                         'error 03')
        self.assertEqual(data['comercial_data'][2],
                         u'Materiales incluidos en el valor del curso.',
                         'error 04')
        self.assertEqual(data['comercial_data'][3],
                         u'Se entrega certificado digital.',
                         'error 05')
        self.assertEqual(data['curso_data'][0], u'Carga horaria 80 horas.',
                         'error 06')
        self.assertEqual(data['curso_data'][1], u'Duración 20 semanas.',
                         'error 07')
        self.assertEqual(data['curso_data'][2], u'<strong>Valor $1200.0 por mes</strong>',
                         'error 08')

        self.assertEqual(data['mode'],u'Son 20 clases de 4 horas c/u','error 085')

        instance = data['instances'][0]
        self.assertEqual(instance['month'], u'Agosto 2016','error 10')
        self.assertEqual(instance['day'], u'1','error 11')
        self.assertEqual(instance['name'],
                         u'[SPX/00] Lun 01/08/16 (12:00 16:00) - Maquillaje Social Profesional','error 12')
        self.assertEqual(instance['weekday'], u'Lunes','error 13')
        self.assertEqual(instance['schedule'], u'12:00 - 16:00 (4hs)','error 14')
        self.assertEqual(instance['vacancy'], u'<p style="color:green;">Vacantes disponibles</p>', 'error 15')

        instance = data['instances'][1]
        self.assertEqual(instance['month'], u'Agosto 2016','error 16')
        self.assertEqual(instance['day'], u'9','error 17')
        self.assertEqual(instance['name'],
                         '[SPX/00] Mar 09/08/16 (15:00 19:00) - Maquillaje Social Profesional','error 18')
        self.assertEqual(instance['weekday'], u'Martes','error 19')
        self.assertEqual(instance['schedule'], u'15:00 - 19:00 (4hs)','error 20')
        self.assertEqual(instance['vacancy'], u'<p style="color:green;">Vacantes disponibles</p>','error 21')


    def test_check_one_lecture(self):
        """ chequea texto cuando hay una o varias clases """

        # creo el producto S23
        ##################################################################################
        self.product1 = self.product_obj.create({
            'tot_hs_lecture': 4,
            'hs_lecture': 4,
            'no_quotes': 1,
            'default_code': 'S23',
            'list_price': 600,
            'type': 'curso',
            'name': 'Glitter',
            'agenda':
                """
                """,
            'description':
                """
                """
        })

        # creo un curso basado en producto 1
        ##################################################################################
        self.curso1 = self.curso_obj.create({
            'product': self.product1.id,
            'main_speaker_id': self.partner_prof.id
        })

        ##################################################################################
        # Se chequea el producto
        data = self.product1.info_curso_html_data(debug=True)
        self.assertEqual(data['mode'], u'Es una clase de 4 horas','error 22')




        # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
