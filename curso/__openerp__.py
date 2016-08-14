# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Organización de Cursos',
    'version': '8.0.1.1.0',
    'category': 'Tools',
    'summary': 'Cursos, Inscripciones, Reservas etc.',
    'description': """
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

This proyect support [semver](http://semver.org/)

Manejo de Cursos en una Academia
================================
El módulo curso le ayuda a manejar y organizar en forma eficiente los cursos \
de una academia.

Puntos Clave
------------
- Definición de los cursos como Productos (servicios)
- Definicion las instancias de los cursos, cada vez que se vuelve a dictar un\
 curso se autoincrementa en nro de instancia.
- Estados de los cursos Borrador, Cursando, Cumplido, Cancelado
- Estados de los alumnos inscriptos en los cursos, Interesado, Señado, \
Cursando, Cumplido, Cancelado
- Historia de las cursadas registradas en la ficha del alumno
- Generación automática de la facturación
- Reporte diario de asistentes con detalle de cuotas adeudadas e información \
faltante en la ficha del alumno
- Vista de calendario de las clases

""",
    'author': 'jeo software',
    'depends': ['base',
                'base_setup',
                'board',
                'email_template',
                'l10n_ar_invoice',
                'document_page',
                'web_widget_text_markdown'],
    'data': [
        'security/curso_security.xml',
        'security/ir.model.access.csv',
        'wizard/add_registration_view.xml',
        'wizard/mail_confirm_view.xml',
        'views/curso_view.xml',
        'views/registration_view.xml',
        'views/engine_view.xml',
        'views/board_association_view.xml',
        'views/res_product_view.xml',
        'views/email_template.xml',
        'views/res_partner_view.xml',
        'wizard/create_invoice_view.xml',
        'wizard/daily_report_view.xml',
        'report/report_curso_registration_view.xml',
        'wizard/move_registration.xml',
        'data/curso_data.xml',
        'curso_report.xml',
        'views/curso_report_incoming.xml',
        'views/report_curso_attendance.xml'
    ],
    #    'demo': ['data/curso_demo.xml'],

    'test': [
        'tests/process/partner_test.yml',
        'tests/process/schedule_test.yml',
        'tests/process/holiday_test.yml',
        'tests/process/curso_test.yml',
        'tests/test_curso1.py'
    ],
    'css': ['static/src/css/curso.css'],
    'js': ['static/src/js/announcement.js'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': [],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
