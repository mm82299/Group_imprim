# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp
import logging
from odoo.tools import float_is_zero

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def create(self, vals):
        line = super(SaleOrderLine, self).create(vals)
        product = self.env['product.product'].browse(vals['product_id'])
        line.write({'price_unit': product.list_price})
        return line
        
    
    

   