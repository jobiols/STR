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
from openerp import api, models

class CursoReportIncoming(models.AbstractModel):
    _name = 'report.curso.curso_report_incoming'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('curso.curso_report_incoming')
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'get_products':self._get_products
        }
        return report_obj.render('curso.curso_report_incoming', docargs)

    @api.one
    def _get_products(self):
        prod = self.env['product.product'].search([('type','=','curso')])
#        print 'cantidad de cursos', len(prod.curso_instances)
#        for curs in prod.curso_instances:
#            print curs.name

#        print 'cantidad productos', len(prod)
        return prod