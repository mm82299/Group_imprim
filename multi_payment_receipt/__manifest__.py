# -*- coding: utf-8 -*-
{
    'name': "Multi Payment Receipt",
    'summary': """ This is the module to print multi payment receipt per client """,
    "contributors": [
        "Sarra RHIM",
    ],
    'author': "ICST",
    'website': "http://www.ics-tunisie.com",
    'depends': [
        'base',
        'account'
    ],
    'data': [
        'views/report_payment_receipt_templates.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': False,
}