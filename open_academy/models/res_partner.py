from odoo import fields, models


class PartnerOpenAcademy(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean(string='Is instructor')
    session_ids = fields.Many2many('open_academy.session', string='Sessions')
