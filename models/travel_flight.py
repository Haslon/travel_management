from odoo import models, fields

class TravelFlight(models.Model):
    _name = 'travel.flight'
    _description = 'Airline Flight'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'departure_datetime desc' # Orden por defecto

    name = fields.Char(string='Flight Identifier', compute='_compute_name', store=True, readonly=True)
    flight_number = fields.Char(string='Flight Number', required=True)
    airline = fields.Char(string='Airline', required=True, help="Name of the airline")
    departure_datetime = fields.Datetime(string='Departure Time', required=True)
    arrival_datetime = fields.Datetime(string='Arrival Time') # Podría ser útil
    destination_id = fields.Many2one(
        'travel.destination',
        string='Destination',
        required=True,
        ondelete='restrict' # No permitir borrar destino si hay vuelos asociados
    )
    origin_id = fields.Many2one( # Podría ser útil un origen
        'travel.destination',
        string='Origin'
    )
    rating_ids = fields.One2many(
        'travel.rating',
        'flight_id',
        string='Ratings',
        domain=[('rated_item_type', '=', 'flight')]
    )
    # Campo para moneda, se usará en paquetes y potencialmente en costos de vuelo
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id', string='Currency', readonly=True)


    def _compute_name(self):
        for flight in self:
            flight.name = f"{flight.airline or ''} {flight.flight_number or ''}"

    _sql_constraints = [
        ('flight_number_departure_uniq', 'unique(flight_number, departure_datetime, airline)',
         'Flight number must be unique for the given airline and departure time.')
    ]

    rating_count = fields.Integer(compute='_compute_rating_stats', string="Rating Count")
    average_flight_rating = fields.Float(compute='_compute_rating_stats', string="Avg. Rating", digits=(3,2))

    @api.depends('rating_ids', 'rating_ids.rating')
    def _compute_rating_stats(self):
        for flight in self:
            ratings = flight.rating_ids.filtered(lambda r: r.rating)
            flight.rating_count = len(ratings)
            if ratings:
                flight.average_flight_rating = sum(r.rating for r in ratings) / len(ratings)
            else:
                flight.average_flight_rating = 0.0

    def action_create_rating(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Rate Flight',
            'res_model': 'travel.rating',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_flight_id': self.id,
                'default_rated_item_type': 'flight',
            }
        }