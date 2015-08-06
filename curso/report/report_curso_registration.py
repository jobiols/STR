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

from openerp.osv import fields, osv
from openerp import tools


class report_curso_registration(osv.osv):
    _name = "report.curso.registration"
    _description = "Cursos Analysis"
    _auto = False
    _columns = {
        'curso_date': fields.char('curso Start Date', size=64, readonly=True),
        'year': fields.char('Year', size=4, readonly=True),
        'month': fields.selection([
            ('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'),
            ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'),
            ('09', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')], 'Month', readonly=True),
        'curso_id': fields.many2one('curso.curso', 'curso', required=True),
        'draft_state': fields.integer(' # Nro de Inscripciones en borrador', size=20),
        'confirm_state': fields.integer(' # Nro de Inscripciones confirmadas', size=20),
        'register_max': fields.integer('Máximo de Inscripciones'),
        'nbcurso': fields.integer('Number Of cursos'),
        'curso_type': fields.many2one('curso.type', 'curso Type'),
        'registration_state': fields.selection(
            [('draft', 'Draft'), ('confirm', 'Confirmed'), ('done', 'Attended'), ('cancel', 'Cancelled')],
            'Registration State', readonly=True, required=True),
        'curso_state': fields.selection(
            [('draft', 'Draft'), ('confirm', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')], 'curso State',
            readonly=True, required=True),
        'user_id': fields.many2one('res.users', 'curso Responsible', readonly=True),
        'user_id_registration': fields.many2one('res.users', 'Register', readonly=True),
        'name_registration': fields.char('Participant / Contact Name', size=45, readonly=True),
        'speaker_id': fields.many2one('res.partner', 'Speaker', readonly=True),
        'company_id': fields.many2one('res.company', 'Company', readonly=True),
    }
    _order = 'curso_date desc'

    def init(self, cr):
        """
        Initialize the sql view for the curso registration
        """
        tools.drop_view_if_exists(cr, 'report_curso_registration')

        # TOFIX this request won't select cursos that have no registration
        cr.execute(""" CREATE VIEW report_curso_registration AS (
            SELECT
                e.id::varchar || '/' || coalesce(r.id::varchar,'') AS id,
                e.id AS curso_id,
                e.user_id AS user_id,
                r.user_id AS user_id_registration,
                r.name AS name_registration,
                e.company_id AS company_id,
                e.main_speaker_id AS speaker_id,
                to_char(e.date_begin, 'YYYY-MM-DD') AS curso_date,
                to_char(e.date_begin, 'YYYY') AS year,
                to_char(e.date_begin, 'MM') AS month,
                count(e.id) AS nbcurso,
                CASE WHEN r.state IN ('draft') THEN r.nb_register ELSE 0 END AS draft_state,
                CASE WHEN r.state IN ('open','done') THEN r.nb_register ELSE 0 END AS confirm_state,
                e.type AS curso_type,
                e.register_max AS register_max,
                e.state AS curso_state,
                r.state AS registration_state
            FROM
                curso_curso e
                LEFT JOIN curso_registration r ON (e.id=r.curso_id)

            GROUP BY
                curso_id,
                user_id_registration,
                r.id,
                registration_state,
                r.nb_register,
                curso_type,
                e.id,
                e.date_begin,
                e.user_id,
                curso_state,
                e.company_id,
                e.main_speaker_id,
                year,
                month,
                e.register_max,
                name_registration
        )
        """)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
