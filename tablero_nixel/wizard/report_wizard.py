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

# constantes
PROVEEDORES = 79
DEUDORES_POR_VENTAS = 8
GASTOS = 155


class report_wizard(orm.TransientModel):
    _name = 'tablero_nixel.wiz_report_nixel'
    _columns = {
        'desde_date': fields.date('Desde'),
        'hasta_date': fields.date('Hasta'),
        'venta_fac': fields.float('venta_fac'),
        'venta_cob': fields.float('venta_cob'),
        'venta_pen': fields.float('venta_pen'),
        'compra_fac': fields.float('compra_fac'),
        'compra_cob': fields.float('compra_cob'),
        'compra_pen': fields.float('compra_pen'),
        'gastos': fields.float('gastos')
    }

    def summarize_account(self, cr, uid, context, account_id):
        partner_obj = self.pool.get('res.partner')
        accounts = self.pool['account.move.line']
        ids = accounts.search(cr, uid, [('account_id', '=', account_id)]
                              , context=context)
        debit = credit = 0.0
        for account in accounts.browse(cr, uid, ids, context):
            debit += account.debit
            credit += account.credit
        return {'debit': debit, 'credit': credit}

    def button_generate_report(self, cr, uid, ids, context=None):
        partner_obj = self.pool.get('res.partner')
        cur_obj = self.browse(cr, uid, ids, context=context)

        dic = self.summarize_account(cr, uid, context, DEUDORES_POR_VENTAS)

        cur_obj.venta_fac = dic['debit']
        cur_obj.venta_cob = dic['credit']
        cur_obj.venta_pen = cur_obj.venta_fac - cur_obj.venta_cob

        dic = self.summarize_account(cr, uid, context, PROVEEDORES)

        cur_obj.compra_cob = dic['debit']
        cur_obj.compra_fac = dic['credit']
        cur_obj.compra_pen = cur_obj.compra_fac - cur_obj.compra_cob

        dic = self.summarize_account(cr, uid, context, GASTOS)
        cur_obj.gastos = dic['debit']

        datas = {}
        if cur_obj.desde_date > cur_obj.hasta_date:
            raise orm.except_orm('Ojo!', 'La fech final (%s) no debe ser menor que \
                la fecha inicial (%s)' % (cur_obj.desde_date, cur_obj.hasta_date))

        partner_ids = partner_obj.search(cr, uid, [], context=context)
        if partner_ids:
            data = self.read(cr, uid, ids, context=context)[0]
            datas = {
                'ids': partner_ids,
                'model': 'tablero_nixel.wiz_report_nixel',  # wizard model name
                'form': data,
                'context': context
            }

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'tablero_nixel.nixel_report',
            'datas': datas,
        }

        # vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
