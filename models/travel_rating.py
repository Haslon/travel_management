from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TravelRating(models.Model):
    _name = 'travel.rating'
    _description = 'Travel Rating and Comments'
    _inherit = ['mail.thread'] # Solo chatter, no actividades por defecto
    _order = 'rating_date desc'

    # Para poder calificar diferentes modelos (Agencia o Vuelo)
    # Usaremos un campo de referencia genérico (res_model, res_id)
    # O dos Many2one separados y una restricción para asegurar que solo uno esté lleno.
    # Optamos por dos M2O separados para mayor simplicidad en vistas y dominios.

    rated_item_type = fields.Selection([
        ('agency', 'Agency'),
        ('flight', 'Flight')
    ], string="Rated Item Type", required=True)

    agency_id = fields.Many2one('travel.agency', string='Agency', ondelete='cascade')
    flight_id = fields.Many2one('travel.flight', string='Flight', ondelete='cascade')

    partner_id = fields.Many2one('res.partner', string='User', required=True, default=lambda self: self.env.user.partner_id)
    rating = fields.Selection([
        ('1', '1 - Very Poor'),
        ('2', '2 - Poor'),
        ('3', '3 - Average'),
        ('4', '4 - Good'),
        ('5', '5 - Excellent')
    ], string='Rating Score', required=True)
    comment = fields.Text(string='Comment', translate=True)
    rating_date = fields.Date(string='Date', required=True, default=fields.Date.context_today)

    @api.constrains('agency_id', 'flight_id', 'rated_item_type')
    def _check_rated_item(self):
        for record in self:
            if record.rated_item_type == 'agency' and not record.agency_id:
                raise ValidationError("If rated item type is 'Agency', an agency must be selected.")
            if record.rated_item_type == 'flight' and not record.flight_id:
                raise ValidationError("If rated item type is 'Flight', a flight must be selected.")
            if record.agency_id and record.flight_id:
                raise ValidationError("A rating can only be for an agency OR a flight, not both.")
            if not record.agency_id and not record.flight_id:
                 raise ValidationError("A rating must be linked to an agency or a flight.")

    # Nombre para visualización
    name = fields.Char(compute='_compute_name', string="Rating Summary", store=True)

    @api.depends('rated_item_type', 'agency_id.name', 'flight_id.name', 'rating')
    def _compute_name(self):
        for rec in self:
            item_name = ""
            if rec.rated_item_type == 'agency' and rec.agency_id:
                item_name = rec.agency_id.name
            elif rec.rated_item_type == 'flight' and rec.flight_id:
                item_name = rec.flight_id.name
            rec.name = f"Rating for {item_name}: {rec.rating} star(s)"