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
from openerp.osv import osv, fields

class curso_move_registration(osv.osv_memory):
    def button_move_registration(self, cr, uid, ids, context=None):
        reg_pool = self.pool['curso.registration']
        for wiz in self.browse(cr, uid, ids, context):
            # verificar que las inscripciones estan canceladas
            for reg in reg_pool.browse(cr, uid, context['active_ids']):
                if reg.state == 'done' or reg.state == 'confirm':
                    raise osv.except_osv(('Error!'), (
                        u"Solo se pueden mover inscripciones en estado interesada, señada y cancelada."))
            # por cada inscripcion marcada cambiarle el curso
            for reg in reg_pool.browse(cr, uid, context['active_ids']):
                reg.curso_id = wiz.curso_id

    def button_copy_registration(self, cr, uid, ids, context=None):
        reg_pool = self.pool['curso.registration']
        for wiz in self.browse(cr, uid, ids, context):
            # por cada inscripcion marcada duplicarla con el nuevo curso
            for reg in reg_pool.browse(cr, uid, context['active_ids']):
                defaults = {
                    'curso_id': wiz.curso_id.id,
                    'user_id': uid,
                    'state': 'draft'
                }
                reg_pool.copy(cr, uid, reg.id, defaults, context=context)

    def create_grid_report(self, cr, uid, ids, cursos, context=None):
        html = u"""
        <table style="width:100%%;">
            <tbody>
            """
        for curso in cursos:
            html += u"""
                <tr>
                    <td width="10%%"><div style="text-align: center;">
                         Inicio<br />%s</div>
                    </td>
                    <td width="72%%" valign="top">
                        <h3><a href="%s">
                        %s<span style="font-size: small;"><sup>&nbsp;Cód %s</sup></span>
                        </a></h3>
                    </td>
                    <td width="8%%">
                        <p>%s hs</p>
                    </td>
                    <td width="10%%">
                        <a href="%s">Más datos</a>
                    </td>
                </tr>
                """ % (curso['date_begin'],
                       curso['product_url'],
                       curso['name'],
                       curso['code'],
                       curso['tot_hs_lecture'],
                       curso['product_url'])

        html += u"""
            </tbody>
        </table>
        """
        rep_name = 'reporte grilla para wordpress'
        # Borrar el documento si es que existe
        doc_pool = self.pool.get('document.page')
        records = doc_pool.search(cr, uid, [('name', '=', rep_name)])
        doc_pool.unlink(cr, uid, records)

        new_page = {
            'name': rep_name,
            'content': html,
        }
        # Generar el documento
        self.pool.get('document.page').create(cr, uid, new_page, context=context)

        print curso

    def button_grid_report(self, cr, uid, ids, context=None):
        curso_obj = self.pool['curso.curso']
        for wiz in self.browse(cr, uid, ids, context):
            # armar una lista con los cursos a reportar
            cursos = []
            for reg in curso_obj.browse(cr, uid, context['active_ids']):
                cursos.append({'name': reg.product.name,
                               'code': reg.default_code,
                               'date_begin': reg.date_begin,
                               'product_url': reg.product.product_url,
                               'tot_hs_lecture': int(reg.tot_hs_lecture)
                               })
            self.create_grid_report(cr, uid, ids, cursos, context)



    _name = "curso.move.registration"
    _description = "Mover inscripciones entre cursos"

    _columns = {
        'curso_id': fields.many2one('curso.curso', 'Curso', required=True),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
