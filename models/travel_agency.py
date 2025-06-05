from odoo import models, fields, api
class TravelAgency(models.Model):
    _name = 'travel.agency'
    _description = 'Travel Agency'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Agency Name', required=True, translate=True)
    partner_id = fields.Many2one('res.partner', string='Related Partner', required=True)
    contact_email = fields.Char(string='Contact Email')
    phone = fields.Char(string='Phone')
    description = fields.Text(string='Description', translate=True)
    destination_ids = fields.Many2many(
        'travel.destination',
        'travel_destination_agency_rel', # Misma tabla de relación que en travel.destination
        'agency_id',
        'destination_id',
        string='Serviced Destinations'
    )
    rating_ids = fields.One2many(
        'travel.rating',
        'agency_id',
        string='Ratings',
        domain=[('rated_item_type', '=', 'agency')]
    )
    # Para el dashboard (se completará con computes más adelante)
    managed_flights_count = fields.Integer(string="Managed Flights Count", compute="_compute_agency_dashboard_stats")
    average_rating = fields.Float(string="Average Rating", compute="_compute_agency_dashboard_stats", digits=(3, 2)) # ej. 4.50

    managing_agency_id = fields.Many2one(
        'travel.agency',
        string='Managing Agency',
        help='Agency that manages this flight'
    )

    def _compute_agency_dashboard_stats(self):
        # Placeholder, la lógica real se implementará cuando existan ratings y reservas
        for agency in self:
            agency.managed_flights_count = 0 # Ejemplo: self.env['travel.flight'].search_count([('agency_id','=',agency.id)])
            agency.average_rating = 0.0 # Ejemplo: calcular desde travel.rating

    # Relacionar con el usuario responsable de la agencia si es necesario
    # user_id = fields.Many2one('res.users', string='Agency Manager')

    @api.depends('rating_ids', 'rating_ids.rating')
    def _compute_agency_dashboard_stats(self):
        Flight = self.env['travel.flight']
        for agency in self:
            # Cuenta los vuelos gestionados por esta agencia
            agency.managed_flights_count = Flight.search_count([('managing_agency_id', '=', agency.id)])
            # Calcula el promedio de calificaciones
            ratings = agency.rating_ids.filtered(lambda r: r.rating)
            if ratings:
                agency.average_rating = sum(r.rating for r in ratings) / len(ratings)
            else:
                agency.average_rating = 0.0