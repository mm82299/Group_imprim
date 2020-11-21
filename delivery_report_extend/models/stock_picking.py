# -*- encoding: utf-8 -*-
##############################################################################
#
#    ODOO, Open Source Management Solution    
#    Copyright (C) 2004-2017 NEXTMA (http://nextma.com). All Rights Reserved
#    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from odoo import fields, api, models, _
from .convertion import trad


class StockPicking(models.Model):

    _inherit = "stock.picking"



    # @api.multi
    @api.depends('sale_id.amount_total')
    def get_amount_letter(self):
        amount = self.company_id.currency_id.amount_to_text(self.sale_id.amount_total)
        return amount
        

    Nom_du_hauffeur = fields.Char(string='Nom du Chauffeur', translate=True)
    immatriculation_camion = fields.Char(string='immatriculation camion', translate=True)
    date_de_Livraison = fields.Date(string="Date de Livraison", required=False)

    # Add amount and taxes to stock pickings

    currency_id = fields.Many2one(
        related="sale_id.currency_id",
        readonly=True,
        string="Currency",
        related_sudo=True,  # See explanation for sudo in compute method
    )
    amount_untaxed = fields.Monetary(
        compute="_compute_amount_all",
        string="Untaxed Amount",
        compute_sudo=True,  # See explanation for sudo in compute method
    )
    amount_tax = fields.Monetary(
        compute="_compute_amount_all", string="Taxes", compute_sudo=True
    )
    amount_total = fields.Monetary(
        compute="_compute_amount_all", string="Total", compute_sudo=True
    )

    def _compute_amount_all(self):
        """This is computed with sudo for avoiding problems if you don't have
        access to sales orders (stricter warehouse users, inter-company
        records...).
        """
        for pick in self:
            round_curr = pick.sale_id.currency_id.round
            amount_tax = 0.0
            for tax_group in pick.get_taxes_values().values():
                amount_tax += round_curr(tax_group["amount"])
            amount_untaxed = sum(
                line.sale_price_subtotal for line in pick.move_line_ids
            )
            pick.update(
                {
                    "amount_untaxed": amount_untaxed,
                    "amount_tax": amount_tax,
                    "amount_total": amount_untaxed + amount_tax,
                }
            )

    def get_taxes_values(self):
        tax_grouped = {}
        for line in self.move_line_ids:
            for tax in line.sale_line.tax_id:
                tax_id = tax.id
                if tax_id not in tax_grouped:
                    tax_grouped[tax_id] = {"base": line.sale_price_subtotal, "tax": tax}
                else:
                    tax_grouped[tax_id]["base"] += line.sale_price_subtotal
        for tax_id, tax_group in tax_grouped.items():
            tax_grouped[tax_id]["amount"] = tax_group["tax"].compute_all(
                tax_group["base"], self.sale_id.currency_id
            )["taxes"][0]["amount"]
        return tax_grouped