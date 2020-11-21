# -*- coding: utf-8 -*-
{
    'name': "Vendor Bills Add Logistic Costs",
    'summary': """ This is the module to add logistic costs in vendor bills """,
    "contributors": [
        "Sarra RHIM",
    ],
    'author': "ICST",
    'website': "http://www.ics-tunisie.com",
    'depends': [
        'base',
        'account',
        'invoice_stock_move',
        'stock_account',
        'stock_landed_costs',
    ],
    'data': [
        'views/account_move.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': False,
 
}