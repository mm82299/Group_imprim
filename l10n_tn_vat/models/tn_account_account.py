from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class Company(models.Model):
    _inherit = "res.company"

    tn_enable_tax = fields.Boolean(string="Activate Tunisia Tax")
    tn_sales_tax_account = fields.Many2one('account.account', string="Sales Tax Account")
    tn_purchase_tax_account = fields.Many2one('account.account', string="Purchase Tax Account")


class TnResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    tn_enable_tax = fields.Boolean(string="Activate Tunisia Tax", related='company_id.tn_enable_tax', readonly=False)
    tn_sales_tax_account = fields.Many2one('account.account', string="Sales Tax Account", related='company_id.tn_sales_tax_account', readonly=False)
    tn_purchase_tax_account = fields.Many2one('account.account', string="Purchase Tax Account", related='company_id.tn_purchase_tax_account', readonly=False)
