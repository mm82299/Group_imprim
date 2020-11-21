# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp
import logging
from odoo.tools import float_is_zero

class AccountInvoice(models.Model):
    _inherit = 'account.move.line'

    other_costs = fields.Float('Autre frais',default=0,compute= '_compute_other_costs')
    cost_price = fields.Float('Prix de revient', default=0, compute='_compute_other_costs')

    @api.depends('product_id','move_id')
    def _compute_other_costs(self):
        for record in self:
            record.other_costs = 0.0
            record.cost_price = 0.0
            if record.move_id.type == 'in_invoice' and record.product_id and record.move_id:
                picking_id = record.move_id.invoice_picking_id
                scraps = self.env['stock.scrap'].search([('picking_id', '=', picking_id.id)])
                valorisation = self.env['stock.valuation.layer'].sudo().search([('id', 'in', (picking_id.move_lines + scraps.move_id).stock_valuation_layer_ids.ids),
                                                                                ('product_id','=',record.product_id.id),
                                                                                ('quantity','=',0)])
                all_valorisations = self.env['stock.valuation.layer'].sudo().search(
                    [('id', 'in', (picking_id.move_lines + scraps.move_id).stock_valuation_layer_ids.ids),
                     ('product_id', '=', record.product_id.id),
                     ])
                total_amount = sum(all_valorisations.mapped('value'))
                total_quantity = record.quantity
                record.other_costs = 0.0
                
                for val in valorisation:
                    record.other_costs += val.value
                if total_amount != 0 and total_quantity != 0:
                    record.cost_price = total_amount/total_quantity
                
                

class AccountMove(models.Model):
    _inherit = 'account.move'


    def _get_default_picking(self):
        ''' Get the default picking from either the purchase order, either false. '''
        purchase_id = self.env.context.get('default_purchase_id')
        purchase_id = self.env['purchase.order'].browse(purchase_id)
        picking = False
        if purchase_id:
            picking = purchase_id.picking_ids.ids[0] if purchase_id.picking_ids else False
        picking = self.env['stock.picking'].browse(picking)
        print(picking,'******************************')
        return picking

    invoice_picking_id = fields.Many2one('stock.picking', string="Picking Id",default=_get_default_picking)

    def action_view_stock_valuation_layers(self):
        if self.invoice_picking_id:
            return self.invoice_picking_id.action_view_stock_valuation_layers()
        else:
            return None
        