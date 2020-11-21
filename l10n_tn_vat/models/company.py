# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    tds_account_id_customer = fields.Many2one(string="Tax Customer retainer account",
                                     comodel_name="account.account")

    tds_account_id_vendor = fields.Many2one(string="Tax Vendor retainer account",
                                              comodel_name="account.account")