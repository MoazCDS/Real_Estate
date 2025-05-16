from email.policy import default

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'

    name = fields.Char(default="New", size=10)
    description = fields.Text()
    postcode = fields.Char(required=True)
    date_availability = fields.Date()
    expected_price = fields.Float()
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], default="north")
    diff = fields.Float(compute="_compute_diff")

    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold')
    ], default="draft")

    _sql_constraints = [
        ('name_key', 'unique("name")', 'This name already exists')
    ]

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms <= 0:
                raise ValidationError('Please enter a valid number of bedrooms')

    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.expected_price - rec.selling_price

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def pending_draft(self):
        for rec in self:
            rec.state = 'pending'

    def sold_draft(self):
        for rec in self:
            rec.state = 'sold'