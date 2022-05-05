from odoo import models, fields, api


class Course(models.Model):
    _name = 'open_academy.course'
    _description = 'Course model'
    name = fields.Char()
    title = fields.Char(required=True)
    description = fields.Text()
    responsible_user_id = fields.Many2one('res.users', string='Responsible')
    session_ids = fields.One2many(
        'open_academy.session', 'course_id', string='Sessions')

    _sql_constraints = [('description_and_title_different',
                         'CHECK(description != title)',
                         'Course description and title must be different'),
                        ('name_unique',
                         'UNIQUE(name)',
                         'Name of course isn''t UNIQUE')]

    def copy(self, default=None):
        default = default if type(default) is dict else {}
        cnt = self.env['open_academy.course'].search_count([
            ('name', '=like', 'Copy of {}%'.format(self.name))])
        cntstr = ' ({})'.format(cnt) if cnt else ''
        default['name'] = 'Copy of {}{}'.format(self.name, cntstr)
        return super(Course, self).copy(default)
