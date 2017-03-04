# -*- coding: utf-8 -*-
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
from openerp import models, fields, api


class curso_woo_categ(models.Model):
    _name = 'curso.woo.categ'
    # esto hace que el name del registro sea path
    _rec_name = 'path'

    path = fields.Char(
            compute="get_path",
            store=True
    )

    woo_id = fields.Integer(
    )

    woo_ids = fields.Char(
            compute="get_woo_ids"
    )

    woo_idx = fields.Integer(
            compute="get_woo_idx",
            store=True
    )

    slug = fields.Char(
    )

    name = fields.Char(
    )

    parent = fields.Many2one(
            'curso.woo.categ',
            string="Parent"
    )

    @api.multi
    def _path(self):
        for cat in self:
            if cat.parent:
                return u'{} / {} '.format(cat.parent._path(), cat.name)
            else:
                return cat.name

    @api.one
    @api.depends('parent', 'name')
    def get_path(self):
        self.path = self._path()

    @api.one
    def get_woo_ids(self):
        ids = []
        ids.append(self.woo_id)
        if self.parent:
            ids.append(self.parent.woo_id)
            if self.parent.parent:
                ids.append(self.parent.parent.woo_id)
        self.woo_ids = ids

    @api.one
    @api.depends('woo_ids')
    def get_woo_idx(self):
        ids = eval(self.woo_ids)
        self.woo_idx = len(ids)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
