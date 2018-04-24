# -*- coding: utf-8 -*-

from odoo import fields, models


class MaritalStatus(models.Model):
    _name = 'marital.status'
    _description = 'https://www.hl7.org/fhir/valueset-marital-status.html'

    name = fields.Char('Display')
    code = fields.Char('Code')
    definition = fields.Char('Definition')
    comments = fields.Text('Comments')

    # TODO: Add a constraint for uniqueness of code


class AdministrativeGender(models.Model):
    _name = 'administrative.gender'
    _description = 'https://www.hl7.org/fhir/valueset-administrative-gender.html'

    name = fields.Char('Display')
    code = fields.Char('Code')
    definition = fields.Char('Definition')
    comments = fields.Text('Comments')

    # TODO: Add a constraint for uniqueness of code


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    gender_id = fields.Many2one(
        'administrative.gender', copy=False,
        help='The gender of a person used for administrative purposes')
    birthdate = fields.Date()
    deceased = fields.Boolean()
    decease_date = fields.Date()
    marital_status_id = fields.Many2one(
        'marital.status', copy=False,
        help='This field contains a patient\'s most recent marital (civil) status')
    multiple_birth = fields.Boolean(help="Whether patient is part of a multiple birth")
    multiple_birth_number = fields.Integer(
        help="Indicates the actual birth order in multiple birth")
