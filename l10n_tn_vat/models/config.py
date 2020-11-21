# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    tds_account_id_customer = fields.Many2one(string="Tax customer retainer account",
                                          comodel_name="account.account",
                                          )
    tds_account_id_vendor = fields.Many2one(string="Tax vendor retainer account",
                                     comodel_name="account.account",
                                     )
    

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        param.set_param('l10n_tn_vat.tds_account_id_customer.id', self.tds_account_id_customer.id)
        self.company_id.tds_account_id_customer = self.tds_account_id_customer.id

        param.set_param('l10n_tn_vat.tds_account_id_vendor.id', self.tds_account_id_vendor.id)
        self.company_id.tds_account_id_vendor = self.tds_account_id_vendor.id
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            tds_account_id_customer=int(params.get_param('l10n_tn_vat.tds_account_id_customer.id')),
            tds_account_id_vendor=int(params.get_param('l10n_tn_vat.tds_account_id_vendor.id')),
        )
        return res