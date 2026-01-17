# -*- coding: utf-8 -*-
{
    'name': 'Mi Módulo de Informes',
    'version': '18.0.1.0.0',
    'summary': 'Módulo ligero para generar informes QWeb en Odoo 18.',
    'author': 'Mariana',
    'license': 'AGPL-3',
    'category': 'Reporting',
    'depends': [
        'base',
        'web',
    ],
    'data': [
        'security/ir.model.access.csv',
        'report/report_template.xml',
        'report/report_action.xml',
        'wizard/report_data_wizard_view.xml',
        'views/report_menu.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
