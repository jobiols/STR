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


class prepare_mass_mail(models.TransientModel):
    """ Wizard para agregar una inscripción de una clienta a un curso """
    _name = 'curso.prepare.mass.mail'
    _description = "pone etiquetas en partners para luego mandar mass mail"

    category_id = fields.Many2one('res.partner.category', string='Tags')

    @api.multi
    def button_prepare(self):
        """ agrega la etiqueta seleccionada a todos los partners que estan seleccionados
        """
        regs = self.env['curso.registration'].browse(self._context['active_ids'])
        for reg in regs:
            reg.partner_id.category_id += self.category_id

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
