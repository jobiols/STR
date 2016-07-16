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
from openerp import models, fields, api


class curso_quota(models.Model):
    _name = 'curso.quota'
    _order = 'date desc'

    registration_id = fields.Many2one('curso.registration', 'Inscripcion', required= True)
    date = fields.Date('Fecha factura')
    list_price = fields.Float('Precio')
    quota = fields.Integer('#cuota', readonly=False)
    invoice_id = fields.Many2one('account.invoice', 'Factura', required=False)
    amount = fields.Char(compute="_get_amount_paid", string='Facturado')
    state = fields.Char(compute="_get_state", string='Estado Factura')
    curso_inst = fields.Char(related='registration_id.curso_id.curso_instance',
                             string='Instancia', readonly=True)
    partner_id = fields.Char(related='registration_id.partner_id.name',
                             string='Alumna', readonly=True)

    @api.one
    def _get_state(self):
        self.state = 'Pendiente'
        if self.invoice_id:
            account_invoice_obj = self.env['account.invoice']
            for invoice in account_invoice_obj.search([('id', '=', self.invoice_id.id)]):
                if invoice.state == 'draft':
                    self.state = 'Borrador'
                if invoice.state == 'paid':
                    self.state = 'Pagado'
                if invoice.state == 'open':
                    self.state = 'Abierto'
                if invoice.state == 'cancel':
                    self.state = 'Cancelado'

    @api.one
    def _get_amount_paid(self):
        self.amount = 0
        if self.invoice_id:
            account_invoice_obj = self.env['account.invoice']
            for invoice in account_invoice_obj.search([('id', '=', self.invoice_id.id)]):
                self.amount = invoice.amount_total

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
