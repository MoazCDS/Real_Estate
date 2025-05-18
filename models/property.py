from email.policy import default

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    _description = 'Property'
    _inherit = ['mail.thread','mail.activity.mixin']

    #To make the chatter track any changes in a specific field add the argument "tracking=True"
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
    diff = fields.Float(compute="_compute_diff", store=True)
    # Readonly=True by default. Store=False by default. It has to be the same type as the thing it's related to
    owner_phone = fields.Char(related='owner_id.phone')
    owner_address = fields.Char(related="owner_id.address")

    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')
    order_ids = fields.One2many('sale.order', 'property_id', string="Orders")
    line_ids = fields.One2many('property.line', 'property_id')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold')
    ], default="draft")

    # If you already had 2 of the same name you have to remove them first or this will not work
    _sql_constraints = [
        ('name_key', 'unique("name")', 'This name already exists')
    ]

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms <= 0:
                raise ValidationError('Please enter a valid number of bedrooms')

# The difference between the depends and the onchange is that the onchange only accepts views fields unlike the depends
# Also in the onchange it returns a sudo record unlike the depends witch return a normal record
    @api.depends('expected_price', 'selling_price', 'owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.expected_price - rec.selling_price

    # @api.onchange('expected_price', 'selling_price')
    # def _compute_diff(self):
    #     for rec in self:
    #         rec.diff = rec.expected_price - rec.selling_price

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            rec.state = 'sold'


class PropertyLines(models.Model):
    _name = 'property.line'

    area = fields.Float()
    description = fields.Char()
    property_id = fields.Many2one('property')