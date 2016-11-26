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
from openerp import models, fields, api
from openerp.osv import osv
from openerp.exceptions import except_orm

class lecture_template(models.Model):
    """ define los contenidos de las clases de cada producto curso """
    _name = 'curso.lecture_template'
    _order = 'seq'

    product_id = fields.Many2one(
        'product.product',
        'Producto'
    )

    text = fields.Text(
        'Contenido de la clase'
    )

    seq = fields.Integer(
        'Sec'
    )

    @api.model
    def create_template(self, prod_id, no_lectures):
        prod_ids = self.search([('product_id', '=', prod_id)])
        if prod_ids:
            raise except_orm(
                'Error!', u"ya existe una plantilla de clases hay que borrarla primero")

        for seq in range(no_lectures):
            new_rec = {
                'product_id': prod_id,
                'seq': seq + 1,
                'text': 'Clase nro %s' % (seq + 1)
            }
            self.create(new_rec)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
