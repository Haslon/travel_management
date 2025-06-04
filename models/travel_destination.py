from odoo import models, fields

class TravelDestination(models.Model):
    _name = 'travel.destination'
    _description = 'Travel Destination'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # Para chatter y actividades

    name = fields.Char(string='Destination Name', required=True, translate=True)
    country_id = fields.Many2one('res.country', string='Country', required=True)
    airport_code = fields.Char(string='Airport Code', size=3) # Ejemplo: LIM, MIA
    description = fields.Text(string='Description', translate=True)
    agency_ids = fields.Many2many(
        'travel.agency',
        'travel_destination_agency_rel', # Nombre de la tabla de relación
        'destination_id', # Columna en la tabla de relación para este modelo
        'agency_id', # Columna en la tabla de relación para el otro modelo
        string='Associated Agencies'
    )

    _sql_constraints = [
        ('airport_code_uniq', 'unique(airport_code, country_id)', 'Airport code must be unique per country!')
    ]