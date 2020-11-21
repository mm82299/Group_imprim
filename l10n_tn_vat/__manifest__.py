# -*- coding: utf-8 -*-
{
    'name': "Tunisia VAT customisations",

    'summary': """
        VAT customisation for Tunisia""",

    'description': """
        Customisations for VAT.
    """,

    'author': "Mourad Meziou",
    'website': "http://www.ics-tunisie.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'base_vat','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/fiscal_position.xml',
        'views/config.xml',
        'views/payment.xml',
        'views/report_invoice.xml',
        'data/account_tax.xml',
        'data/fiscal_position.xml',
	    'views/report_invoicel.xml',
        'views/report_quote.xml',
        'views/tn_account_account.xml',
        'views/tn_account_invoice_supplier_form.xml',
        'views/assets.xml',
    ],
    # only loaded in demonstration mode

}
