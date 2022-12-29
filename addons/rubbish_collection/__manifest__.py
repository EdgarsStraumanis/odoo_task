# -*- coding: utf-8 -*-

{
    'name': 'Rubbish collection',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Rubbish and volunteer management',
    'depends': ['web'],
    'data': [

        'security/ir.model.access.csv',
        'security/security.xml',
        # 'data/data.xml',
        'views/collection_views.xml',
        'views/volunteer_views.xml',
    ],
    'demo': [
        'data/demo.xml',
    ],
    'css': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}