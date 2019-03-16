# -*- coding: utf-8 -*-
########################################################################333###
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
########################################################################333###
{
    'name': 'Makeover',
    'version': '8.0.1.1.0',
    'category': 'Tools',
    'summary': 'Customización Makeover Lab',
    'author': 'jeo software',
    'depends': [
        'base',
        'sale_order_recalculate_prices',
        'web_widget_text_markdown',
        'account_clean_cancelled_invoice_number',
        'stock',
        'purchase',
        'curso',
        'product',
        'nube_connection',
        'base'
    ],
    'data': [
        'views/partner_view.xml',
        'views/hide_fields.xml',
        'security/security_groups.xml',
    ],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': [],

    'repos': [
        {'usr': 'jobiols', 'repo': 'odoo-addons', 'branch': '8.0'},
        {'usr': 'jobiols', 'repo': 'cursos', 'branch': '8.0'},
        # TODO ver que hace este repo que lo borre...
#        {'usr': 'jobiols', 'repo': 'odoomrp-wip', 'branch': '8.0'},

    ],
    'docker': [
        {'name': 'aeroo', 'usr': 'jobiols', 'img': 'aeroo-docs'},
        {'name': 'odoo', 'usr': 'jobiols', 'img': 'odoo-jeo', 'ver': '8.0'},
        {'name': 'postgres', 'usr': 'postgres', 'ver': '9.5'},
        {'name': 'nginx', 'usr': 'nginx', 'ver': 'latest'},
    ],

    'port': '8068'

}

