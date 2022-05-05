from email.policy import default
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Session(models.Model):
    _name = 'open_academy.session'
    _description = 'Course session'
    name = fields.Char()
    start_date = fields.Date(default=lambda self: fields.Date.today())
    duration = fields.Integer()
    number_of_seats = fields.Integer()
    percent_of_taken_seats = fields.Integer(
        compute='_compute_percent_of_taken_seats')
    instructor_id = fields.Many2one('res.partner',
                                    domain=['|',
                                            ('instructor', '=', True),
                                            ('category_id.name', 'ilike', 'Teacher / Level')]
                                    )
    course_id = fields.Many2one('open_academy.course', required=True)
    attendees_ids = fields.Many2many('res.partner', string='Attendees')
    active = fields.Boolean(default=True)

    @api.depends('attendees_ids', 'number_of_seats')
    def _compute_percent_of_taken_seats(self):

        for record in self:
            quantity_of_attendees = len(record.attendees_ids)
            if (quantity_of_attendees == 0) or (record.number_of_seats == 0):
                record.percent_of_taken_seats = 0
            else:
                record.percent_of_taken_seats = quantity_of_attendees/record.number_of_seats*100

    # onchange handler
    @api.onchange('number_of_seats')
    def _onchange_number_of_seats(self):

        if self.number_of_seats <= 0:
            return {
                'warning': {
                    'title': "Incorrect data",
                    'message': "Number of seats must be positive",
                    'type': 'warning'
                }
            }

    # onchange handler
    @api.onchange('attendees_ids')
    def _onchange_attendees_ids(self):

        if len(self.attendees_ids) > self.number_of_seats:
            return {
                'warning': {
                    'title': "Incorrect data",
                    'message': "Quantity of attendees is more than number of seats",
                    'type': 'warning'
                }
            }

    @api.constrains('instructor_id', 'attendees_ids')
    def _check_something(self):
        for record in self:
            for cur_attendee in record.attendees_ids:
                if cur_attendee == record.instructor_id:
                    raise ValidationError(
                        "Instructor can't be an attendee in its course")
