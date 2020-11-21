# -*- coding:utf-8 -*-
#
#
#    Copyright (C) 2015 Clear ICT Solutions <info@clearict.com>.
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify it
#    under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

from odoo import fields, models, api



class LandedCostLinesInherit(models.Model):

    _inherit = 'stock.landed.cost.lines'
 #   split_method = fields.Selection(SPLIT_METHOD, string='Split Method', default = 'by_current_cost_price', required=True)

    @api.onchange('product_id')
    def onchange_product_id(self):
        if not self.product_id:
            self.quantity = 0.0
        self.name = self.product_id.name or ''
        self.split_method = self.split_method or 'by_current_cost_price'
        self.price_unit = self.product_id.standard_price or 0.0
        accounts_data = self.product_id.product_tmpl_id.get_product_accounts()
        self.account_id = accounts_data['stock_input']

    # @api.onchange('product_id')
    # def onchange_product_id(self):
    #     if not self.product_id:
    #         self.quantity = 0.0
    #     self.name = self.product_id.name or ''
    #     self.split_method = self.split_method or 'by_current_cost_price'
    #     self.price_unit = self.product_id.standard_price or 0.0
    #     accounts_data = self.product_id.product_tmpl_id.get_product_accounts()
    #     self.account_id = accounts_data['stock_input']
class AccountMoveInherit(models.Model):

    _inherit = 'account.move'

    def button_create_landed_costs(self):
        """Create a `stock.landed.cost` record associated to the account move of `self`, each
        `stock.landed.costs` lines mirroring the current `account.move.line` of self.
        """
        self.ensure_one()
        landed_costs_lines = self.line_ids.filtered(lambda line: line.is_landed_costs_line)

        landed_costs = self.env['stock.landed.cost'].create({
            'vendor_bill_id': self.id,
            'cost_lines': [(0, 0, {
                'product_id': l.product_id.id,
                'name': l.product_id.name,
                'account_id': l.product_id.product_tmpl_id.get_product_accounts()['stock_input'].id if self.company_id.anglo_saxon_accounting else l.account_id.id,
                'price_unit': l.currency_id._convert(l.price_subtotal, l.company_currency_id, l.company_id, l.move_id.date),
                'split_method': 'by_current_cost_price',
            }) for l in landed_costs_lines],
        })
        action = self.env.ref('stock_landed_costs.action_stock_landed_cost').read()[0]
        return dict(action, view_mode='form', res_id=landed_costs.id, views=[(False, 'form')])
