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

from openerp.tests.common import TransactionCase
import pprint
pp = pprint.PrettyPrinter(indent=4)

# testear con
# ./odooenv.py -Q cursos test_curso2.py -c makeover -d makeover_travis -m curso
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
        self.add_registration_obj = self.env['curso.add_registration']

    def test_add_registration(self):
        """ chequea el agregado de una registración """
        # creo una alumna
        partner = self.partner_obj.create({
            'name': 'Juana Perez Alumna'})

        # creo una profesora
        partner_prof = self.partner_obj.create({
            'name': 'Juana Perez Alumna'})

        # creo un template de mail
        email_template_1 = self.email_template_obj.create({
            'name': 'plantilla de mail'
        })

        # creo un producto
        product = self.product_obj.create({
            'tot_hs_lecture': 15,
            'hs_lecture': 5,
            'no_quotes': 10,
            'default_code': 'SPR',
            'list_price': 800,
            'type': 'curso',
            'name': 'Curso de maquillaje Social Profesional rafañuso',
            'agenda': 'Titulo Cuerpo del texto **negrita** Año 2016',
            'description': 'este es un curso **de prueba** para el test en UTF8 ajá tomá ñoño'
        })

        # creo un curso
        curso = self.curso_obj.create({
            'product': product.id,
            'main_speaker_id': partner_prof.id,
            'email_registration_id': email_template_1.id
        })

        # le agrego la fecha al curso
        curso.date_begin = '2016-01-11'

        # creo el horario
        schedule = self.schedule_obj.create({
            'start_time': 12.5,
            'end_time': 15.5
        })

        # creo una agenda
        self.diary = self.diary_obj.create({
            'curso_id': curso.id,
            'weekday': '1',
            'seq': 1,
            'schedule': schedule.id
        })

        # creo una plantilla de clases para este producto
        product.button_generate_lecture_templates()

        # creo el wizard
        wiz = self.add_registration_obj.create({
            'curso_id': curso.id
        })

        # agrego la registracion
        wiz.with_context({'active_ids':[partner.id]}).button_add_curso()

        reginstration = self.registration_obj.search([])
        for reg in reginstration:
            # la alumna seña el curso
            reg.button_reg_sign()

        # chequear el nombre de las clases
        for ix, lec in enumerate(curso.lecture_ids):
            # chequear el nombre de la clase
            self.assertEqual(lec.name,'Clase nro {}'.format(ix+1),'nombre de la clase')
            # verificar que tenga registros de asistencia
            self.assertNotEqual(len(lec.assistance_id),0,'la clase no tiene asistentes')
            for ass in lec.assistance_id:
                # verificar que la asistente sea Juana
                self.assertEqual(ass.partner_id.name,'Juana Perez Alumna')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
