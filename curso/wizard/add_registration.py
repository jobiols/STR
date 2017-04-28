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


class add_registration(models.TransientModel):
    """ Wizard para agregar una inscripción de una clienta a un curso """

    _name = 'curso.add_registration'
    _description = "Inscribir alumna en curso"

    curso_id = fields.Many2one(
            'curso.curso',
            string="Curso",
            required=True,
            domain="[('register_avail','>','0'), ('next','=',True)]"
    )

    discount = fields.Float(
            'Descuento (%)', digits=(2, 2))

    disc_desc = fields.Char(
            'Razon del descuento', size=128, select=True)

    source = fields.Selection([
        ('none', 'Sin descuento'),
        ('normal', 'Descuento normal'),
        ('groupon', 'Descuento groupon'),
    ],
            'Origen', required=True,
            default='none')

    @api.one
    def button_add_curso(self):
        """ Agrega un curso a la ficha de la alumna, y la pone como interesada
        """
        #  obtener el id de la alumna que viene en el contexto
        partner_ids = self._context.get('active_ids')

        # Crear la inscripcion y agregarla
        vals = {
            'curso_id': self.curso_id.id,
            'partner_id': partner_ids[0],
            'user_id': self._uid,
            'discount': self.discount,
            'disc_desc': self.disc_desc,
        }
        self.env['curso.registration'].create(vals)

    # TODO poner los descuentos en una tabla de configuracion DUPLICADO!!
    @api.onchange('source')
    def _compute_source(self):
        for rec in self:
            if rec.source == 'groupon':
                rec.discount = 73.42
                rec.disc_desc = 'Descuento groupon'
            if rec.source == 'normal':
                rec.discount = 33.333333
                rec.disc_desc = 'Descuento normal'

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
