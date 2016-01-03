# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution.
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>...
#
##############################################################################
from openerp.osv import fields, osv

class curso_quota(osv.osv):
    def _get_state(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for quota in self.browse(cr, uid, ids, context=context):
            res[quota.id] = 'Pendiente'
            register_pool = self.pool.get('account.invoice')
            if quota.invoice_id:
                records = register_pool.search(cr, uid,
                                               [('id', '=', quota.invoice_id.id)])
                for reg in register_pool.browse(cr, uid, records, context):
                    if reg.state == 'draft':
                        res[quota.id] = 'Borrador'
                    if reg.state == 'paid':
                        res[quota.id] = 'Pagado'
                    if reg.state == 'open':
                        res[quota.id] = 'Abierto'
                    if reg.state == 'cancel':
                        res[quota.id] = 'Cancelado'
        return res

    def _get_amount_paid(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for quota in self.browse(cr, uid, ids, context=context):
            res[quota.id] = 0
            register_pool = self.pool.get('account.invoice')
            if quota.invoice_id:
                records = register_pool.search(cr, uid,
                                               [('id', '=', quota.invoice_id.id)])
                for reg in register_pool.browse(cr, uid, records, context):
                    res[quota.id] = reg.amount_total
        return res

#   Curso Quota
    _name = 'curso.quota'
    _description = __doc__
    _columns = {
        'registration_id': fields.many2one('curso.registration', 'Inscripcion'),
        'date': fields.date('Fecha factura'),
        'amount': fields.function(_get_amount_paid, fnct_search=None, string='Facturado',
                                  method=True, store=False,
                                  type='char'),
        'state': fields.function(_get_state, fnct_search=None, string='Estado Factura',
                                 method=True, store=False,
                                 type='char'),
        'list_price': fields.float('Precio'),
        'quota': fields.integer('#cuota', readonly=False),
        'curso_inst': fields.related('registration_id', 'curso_id', 'curso_instance',
                                     string='Instancia', type='char',
                                     size=128, readonly=True),
        'partner_id': fields.related('registration_id', 'partner_id', 'name',
                                     string='Alumna', type='char', size=128,
                                     readonly=True),
        'invoice_id': fields.many2one('account.invoice', 'Factura', required=False),
    }
    _order = 'date desc'

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
