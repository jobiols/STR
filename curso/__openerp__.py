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
    'version': '8.0.2.0.0',
    'category': 'Tools',
    'summary': 'Cursos, Inscripciones, Reservas etc.',
    'author': 'jeo software',
    'depends': ['base',
                'base_setup',
                'board',
                'email_template',
                'l10n_ar_invoice',
                'document_page',
                'web_widget_text_markdown',
                'nube_connection',
                ],
    'data': [
        'security/curso_security.xml',
        'security/ir.model.access.csv',
        'wizard/add_registration_view.xml',
        'wizard/mail_confirm_view.xml',
        'views/curso_view.xml',
        'views/registration_view.xml',
        'views/engine_view.xml',
        'views/lectures_view.xml',
        'views/board_association_view.xml',
        'views/res_product_view.xml',
        'views/email_template.xml',
        'wizard/add_recover_view.xml',
        'views/res_partner_view.xml',
        'wizard/create_invoice_view.xml',
        'wizard/daily_report_view.xml',
        'report/report_curso_registration_view.xml',
        'wizard/move_registration.xml',
        'data/curso_data.xml',
        'curso_report.xml',
        'views/curso_report_incoming.xml',
        'views/report_curso_attendance.xml',
        'wizard/send_mail_view.xml',
        'wizard/prepare_mass_mail_view.xml',
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
