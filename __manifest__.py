# travel_management/__manifest__.py
{
    'name': 'Travel Management',
    'version': '1.0',
    'summary': 'Manage airline travels, travel agencies, and tour packages.',
    'description': """
        Module to manage flight information, travel agencies, ratings,
        tour packages, and related reports.
        Includes multi-language and multi-currency support.
    """,
    'author': 'GersonArcentales/Arcen',
    'website': 'https://www.tuwebsite.com',
    'category': 'Services/Travel',
    'depends': [
        'base',  # Dependencia base de Odoo
        'mail',  # Para chatter (seguimiento, mensajes) y actividades
        'account', # Para multi-moneda y posiblemente facturación futura
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/travel_management_security.xml',
        'views/travel_destination_views.xml',
        'views/travel_flight_views.xml',
        'views/travel_agency_views.xml',
        'views/travel_rating_views.xml',
        'views/travel_package_views.xml',
        'views/travel_management_menus.xml',
        'report/travel_report_templates.xml',   # <-- Añade esto si no está
        'report/travel_reports.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    # Configuración para multi-idioma (Odoo detecta los .po en i18n)
    # Configuración para multi-moneda (se maneja a través de 'account' y campos Monetary)
}