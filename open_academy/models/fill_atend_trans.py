from odoo import models, fields, api


class Course(models.TransientModel):
    _name = 'open_academy.fill_atend_trans'
    _description = 'Wizard with session and partners models'
    name = fields.Char()

    def _default_session(self):
        return self.env['open_academy.session'].browse(self._context.get('active_id'))

    session_id = fields.Many2many(
        'open_academy.session', default=_default_session)
    attendees_ids = fields.Many2many('res.partner')

    def add_partner_list(self):
        for session in self.session_id:
            session.attendees_ids |= self.attendees_ids
        return {}
