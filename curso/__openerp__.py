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
    'version': '8.0.1.0',
    'category': 'Tools',
    'summary': 'Cursos, Inscripciones, Reservas etc.',
    'description': """
Manejo de Cursos en una Academia
================================
El módulo curso le ayuda a manejar y organizar en forma eficiente los cursos de una \
academia.

Puntos Clave
------------
- Definición de los cursos como Productos (servicios)
- Definicion las instancias de los cursos, cada vez que se vuelve a dictar un curso \
se autoincrementa en nro de instancia.
- Estados de los cursos Borrador, Cursando, Terminado, Cancelado
- Estados de los alumnos inscriptos en los cursos, Interesado, Señado, Cursando, \
Terminado, Cancelado
- Historia de las cursadas registradas en la ficha del alumno
- Generación automática de la facturación
- Reporte diario de asistentes con detalle de cuotas adeudadas e información faltante \
en la ficha del alumno
- Vista de calendario de las clases

""",
    'author': 'jeo software',
    'depends': ['base_setup', 'board', 'email_template', 'sale', 'purchase',
                'l10n_ar_invoice'],
    'data': [
        'security/curso_security.xml',
        'security/ir.model.access.csv',
        # 'wizard/curso_confirm_view.xml',

        'wizard/add_registration_view.xml',

        'views/curso_view.xml',
        'views/engine_view.xml',
        'views/board_association_view.xml',
        'views/res_product_view.xml',
        'views/email_template.xml',
        'views/res_partner_view.xml',
        'wizard/create_invoice_view.xml',
        'wizard/daily_report_view.xml',

        'report/report_curso_registration_view.xml',

        'data/curso_data.xml',
    ],
    # 'demo': ['data/curso_demo.xml'],
    'test': ['test/process/curso_test.yml'],
    'css': ['static/src/css/curso.css'],
    'js': ['static/src/js/announcement.js'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': [],
}
# TODO arreglar el curso_demo.xml
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
