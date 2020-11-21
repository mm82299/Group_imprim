
{
    'name': "Journal Restrictions",
    'summary': """Restrict users to certain journals""",
    'description': """Restrict users to certain journals.""",
    'author': "Mourad Meziou",
    'website': "http://ics-tunisie.com/",
    'category': 'account',
    'version': '13.0.0.0',
    'depends': ['account','sale','purchase'],
    'data': [
        'views/users.xml',
        'security/security.xml',
    ],
    "images": [
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
