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

import time

from openerp.osv import osv
from openerp.report import report_sxw


class sale_quotation_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(sale_quotation_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_total': self._get_total,
        })


def _get_total(self, lines, field):
    total = 0.0
    for line in lines:
        total += line.product_uom_qty or 0.0
    return total


class report_saleorderqweb(osv.AbstractModel):
    _name = 'module_name.report_sale_order_qweb'
    _inherit = 'report.abstract_report'
    _template = 'module_name.report_sale_order_qweb'
    _wrapped_report_class = sale_quotation_report

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
