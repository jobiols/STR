# -*- coding: utf-8 -*-
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
########################################################################################
from openerp.osv import fields, osv


class lecture_template(osv.osv):
    """ define los contenidos de las clases de cada producto curso """
    _name = 'curso.lecture_template'
    _order = 'seq'

    _columns = {
        'product_id': fields.many2one('product.product', 'Producto'),
        'text': fields.text('Contenido de la clase'),
        'seq': fields.integer('Sec')
    }

    def create_template(self, cr, uid, ids, no_lectures):
        print 'create template >>>>', no_lectures
        prod_ids = self.search(cr, uid, [('product_id', '=', ids[0])])
        if prod_ids:
            raise osv.except_osv(
                'Error!', u"ya existe una plantilla de clases hay que borrarla primero")

        for seq in range(no_lectures):
            print ids[0], seq
            new_rec = {
                'product_id': ids[0],
                'seq': seq,
                'text': 'Clase nro %s' % (seq + 1)
            }
            self.create(cr, uid, new_rec)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
