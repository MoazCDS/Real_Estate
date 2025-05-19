from odoo import models, fields


class Building(models.Model):
    _name = 'building'
    _description = 'Building'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(required=True)
    no = fields.Integer()
    code = fields.Char()
    description = fields.Text()
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('no_key', 'unique("no")', 'This number already exists'),
        ('code_key', 'unique("code")', 'This code already exists')
    ]