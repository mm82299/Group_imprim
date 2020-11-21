from odoo import models, fields, api, exceptions, _


class account_payment(models.Model):

    _inherit = 'account.payment'

    tds_perc = fields.Float(string="TDS Percentage")
    original_amount = fields.Float(string="Original amount")

    @api.onchange('tds_perc')
    def tds_perc_onchange(self):
        for payment in self:
            move_id = self.env['account.move'].browse(self._context.get('active_ids')).filtered(
                lambda move: move.is_invoice(include_receipts=True))
            if self.tds_perc:
                if move_id.type in ['in_invoice', 'in_refund']:
                    data = {'amount': payment.original_amount * (100 - self.tds_perc) / 100,
                            'writeoff_account_id': self.env.user.company_id.tds_account_id_vendor.id,
                            'payment_difference_handling': 'reconcile',
                            'writeoff_label': 'Tax deduction at source'}
                if move_id.type in ['out_invoice', 'out_refund']:
                    data = {'amount': payment.original_amount * (100 - self.tds_perc) / 100,
                            'writeoff_account_id': self.env.user.company_id.tds_account_id_customer.id,
                            'payment_difference_handling': 'reconcile',
                            'writeoff_label': 'Tax deduction at source'}
                
            else:
                data = {'amount': payment.original_amount,
                        'writeoff_account_id': False,
                        'payment_difference_handling': 'open',
                        'writeoff_label': 'Write-Off'}   
            payment.update(data)

    @api.model
    def default_get(self, fields):
        rec = super(account_payment, self).default_get(fields)
        rec.update({'original_amount': rec.get('amount')})
        return rec