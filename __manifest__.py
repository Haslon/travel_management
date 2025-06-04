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
        # Views se añadirán en la Fase 2
        # Reports se añadirán en la Fase 4
        # Demo data se añadirá en la Fase 5
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    # Configuración para multi-idioma (Odoo detecta los .po en i18n)
    # Configuración para multi-moneda (se maneja a través de 'account' y campos Monetary)
}