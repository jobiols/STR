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

from openerp.osv import orm, fields

class report_wizard(orm.TransientModel):
    _name = 'tablero_nixel.wiz_report_nixel'
    _columns = {
        'desde_date': fields.date('Desde'),
        'hasta_date': fields.date('Hasta'),
    }

    def button_generate_report(self, cr, uid, ids, context=None):
        partner_obj = self.pool.get('res.partner')
        cur_obj = self.browse(cr, uid, ids, context=context)

        datas = {}
        #        if cur_obj.desde_date >= cur_obj.hasta_date:
        #            raise orm.except_orm('Ojo!', 'La fech final (%s) debe ser mayor que \
        #            la fecha inicial (%s)' % (cur_obj.desde_date, cur_obj.hasta_date))

        partner_ids = partner_obj.search(cr, uid, [], context=context)
        if partner_ids:
            data = self.read(cr, uid, ids, context=context)[0]
            print 'data >>', data
            datas = {
                'ids': partner_ids,
                'model': 'tablero_nixel.wiz_report_nixel',  # wizard model name
                'form': data,
                'context': context
            }
        print '-------------------->', datas
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'tablero_nixel.report_demo_nixel',
            # module name.report template name
            'datas': datas,
        }















        # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
