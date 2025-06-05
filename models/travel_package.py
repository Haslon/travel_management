from odoo import models, fields, api

class TravelPackage(models.Model):
    _name = 'travel.package'
    _description = 'Touristic Package'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Package Name', required=True, translate=True)
    description = fields.Text(string='Description', translate=True)
    price = fields.Monetary(string='Price', required=True, currency_field='currency_id')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id', string='Currency', readonly=True)

    flight_ids = fields.Many2many(
        'travel.flight',
        'travel_package_flight_rel',
        'package_id',
        'flight_id',
        string='Included Flights'
    )
    # Campo para otros servicios (texto por ahora, podría ser un O2M a un modelo 'travel.service' en el futuro)
    other_services_description = fields.Html(string='Other Services (e.g., Hotel, Tours)', translate=True)
    active = fields.Boolean(default=True) # Para archivar paquetes

    # Podríamos añadir una agencia asociada al paquete
    # agency_id = fields.Many2one('travel.agency', string='Managing Agency')