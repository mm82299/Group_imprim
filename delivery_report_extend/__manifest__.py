# Copyright 2019 Tecnativa S.L. - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Delivery Report Extend',
    'version': '13.0',
    'category': 'Stock',
    'author': 'Mourad Meziou'
              'Infotech Consulting Services (ICS)',
    'website': 'https://www.ics-tunisie.com',
    'license': 'AGPL-3',
    'depends': [
        'stock','sale_management'
    ],
    'data': [
        'views/stock_picking_view.xml',
        'views/report_deliveryslip.xml',
    ],
    'application': False,
    'installable': True,
}
