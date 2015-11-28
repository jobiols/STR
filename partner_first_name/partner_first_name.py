# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class res_partner(osv.osv):
    _inherit = "res.partner"

    def _get_first_name(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for partner in self.browse(cr, uid, ids, context=context):
            res[partner.id] = partner.name.split(' ', 1)[0]
        return res

    _columns = {
        'first_name': fields.function(
            _get_first_name, fnct_search=None, string='First Name',
            method=True, store=True,
            type='char'),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
