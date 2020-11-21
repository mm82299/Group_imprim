from odoo import models, fields, api, _


class StockValuation(models.Model):
    _inherit = 'stock.valuation.layer'
    @api.model
    def create(self,vals):
        stock_move_id = self.env['stock.move'].browse(vals['stock_move_id'])
        purchase_line_id = stock_move_id.purchase_line_id
        purchase_id = purchase_line_id.order_id
        if purchase_id.active_manual_currency_rate and purchase_id.manual_currency_exchange_rate != 0:
            vals['unit_cost'] = purchase_line_id.price_unit  * purchase_id.manual_currency_exchange_rate
            total = vals['unit_cost'] * purchase_line_id.product_qty
            vals['value'] =  purchase_id.currency_id.round(total)
        result = super(StockValuation, self).create(vals)
        return result


