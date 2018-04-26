# -*- coding: utf-8 -*-

from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


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

    @api.multi
    def _episode_total(self):
        episode_obj = self.env['healthcare.episode']
        for partner in self:
            partner.total_episodes = len(episode_obj.search([('patient_id', '=', partner.id)]))

    patient = fields.Boolean()
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
    general_practitioner_id = fields.Many2one(
        'res.partner', copy=False,
        help="Patient's nominated primary care provider")
    age = fields.Char(compute='_compute_age')
    age_years = fields.Integer(
        string="Age (years old)",
        compute='_compute_age',
        search='_search_age')
    total_episodes = fields.Integer(compute='_episode_total')

    @api.multi
    def _compute_age(self):
        """ Age computed depending based on the birth date in the
         membership request.
        """
        now = datetime.now()
        for record in self:
            if record.birthdate:
                birthdate = fields.Datetime.from_string(
                    record.birthdate,
                )
                if record.deceased:
                    decease_date = fields.Datetime.from_string(record.decease_date)
                    delta = relativedelta(decease_date, birthdate)
                    deceased = _(' (deceased)')
                else:
                    delta = relativedelta(now, birthdate)
                    deceased = ''
                years_months_days = '%d%s %d%s %d%s%s' % (
                    delta.years, _('y'), delta.months, _('m'),
                    delta.days, _('d'), deceased
                )
                years = delta.years
            else:
                years_months_days = _('No DoB')
                years = False
            record.age = years_months_days
            if years:
                record.age_years = years

    def _search_age(self, operator, value):
        if operator not in ('ilike', '=', '>=', '>', '<', '<='):
            raise UserError(_('Invalid operator: %s' % (operator,)))

        current_date = date.today()
        last_birthdate = current_date + relativedelta(years=value * -1)
        first_birthdate = current_date + relativedelta(
            years=(value + 1) * -1,
            days=1,
        )
        last_possible_birthdate = fields.Datetime.to_string(last_birthdate)
        first_possible_birthdate = fields.Datetime.to_string(first_birthdate)

        if operator == '=' or operator == 'ilike':
            return ['&', ('birthdate', '>=', first_possible_birthdate),
                    ('birthdate', '<=', last_possible_birthdate)]
        elif operator == '>=':
            return [('birthdate', '<=', last_possible_birthdate)]
        elif operator == '>':
            return [('birthdate', '<', first_possible_birthdate)]
        elif operator == '<=':
            return [('birthdate', '>=', first_possible_birthdate)]
        elif operator == '<':
            return [('birthdate', '>', last_possible_birthdate)]
    @api.multi
    def action_view_healthcare_episode(self):
        self.ensure_one()
        action = self.env.ref('chet_patient.action_healthcare_episode').read()[0]
        action['domain'] = [('patient_id', '=', self.id)]
        action['context'] = {'default_patient_id': self.id}
        return action
