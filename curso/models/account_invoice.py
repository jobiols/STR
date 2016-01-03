# -*- coding: utf-8 -*-
#################################################################################
from datetime import datetime, timedelta
from openerp.osv import fields, osv
from openerp import models

# hacer que la ultima factura quede arriba
class account_invoice(models.Model):
    _inherit = "account.invoice"
    _order = 'id desc'

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: