# -*- coding: utf-8 -*-

from odoo import fields, models


class InfrastructureBed(models.Model):
    _name = 'infrastructure.bed'

    name = fields.Char('Bed Name')
    code = fields.Char()
    location_id = fields.Many2one(
        'infrastructure.location',
        help="Building this bed is assigned to.")
    state = fields.Selection([
            ('active', 'Active'),
            ('maintenance', 'Maintenance'),
            ('damaged', 'Damaged'),
        ], string='Status', index=True, readonly=True, default='active',)
    # TODO: Add a constraint for uniqueness of code


class InfrastructureLocation(models.Model):
    _name = 'infrastructure.location'

    name = fields.Char()
    code = fields.Char()
    # TODO: Add a constraint for uniqueness of code


class HealthcareEpisode(models.Model):
    _name = 'healthcare.episode'
    _rec_name = 'patient_id'

    # def _default_encounter_ids(self):
    #     bed_id = self.env['infrastructure.bed'].search([('state','=','active')],limit=1)
    #     return [(0, 0, {
    #         'bed_id': bed_id.id,
    #         'date_start': fields.Datetime.now(),
    #     })]

    patient_id = fields.Many2one(
        'res.partner', required=True,
        help="The patient who is in the focus of this episode of care.")
    date_start = fields.Datetime(
        'Start Date', default=fields.Datetime.now, required=True)
    date_end = fields.Datetime('End Date')
    encounter_ids = fields.One2many(
        'healthcare.encounter', 'episode_id', string='Encounters', copy=False,
        # default=_default_encounter_ids
    )

    # http://hl7.org/fhir/episode-of-care-status
    state = fields.Selection([
            ('planned','Planned'),
            ('waitlist', 'Waitlist'),
            ('active', 'Active'),
            ('onhold', 'On Hold'),
            ('finished', 'Finished'),
            ('cancelled', 'Cancelled'),
            ('entered-in-error', 'Entered in Error'),
        ], string='Status', index=True, readonly=True, default='waitlist',
        track_visibility='onchange', copy=False,
        help="Planned: This episode of care is planned to start at the date specified in the period.start. During this status, an organization may perform assessments to determine if the patient is eligible to receive services, or be organizing to make resources available to provide care services.\n"
             "Waitlist: This episode has been placed on a waitlist, pending the episode being made active (or cancelled).\n"
             "Active: This episode of care is current.\n"
             "On Hold: This episode of care is on hold, the organization has limited responsibility for the patient (such as while on respite).\n"
             "Finished: This episode of care is finished and the organization is not expecting to be providing further care to the patient.\n"
             "Cancelled: The episode of care was cancelled, or withdrawn from service, often selected during the planned stage as the patient may have gone elsewhere, or the circumstances have changed and the organization is unable to provide the care. It indicates that services terminated outside the planned/expected workflow.\n"
             "Entered in Error: This instance should not have been part of this patient's medical record.\n")


class HealthcareEncounter(models.Model):
    _name = 'healthcare.encounter'
    _rec_name = 'patient_id'

    episode_id = fields.Many2one(
        'healthcare.episode',
        help="Episode of care this encounter should be recorded against.")
    patient_id = fields.Many2one(
        'res.partner', related='episode_id.patient_id', store=True)
    bed_id = fields.Many2one(
        'infrastructure.bed',
        help="Bed assigned to the patient in this encounter.")
    location_id = fields.Many2one(
        'infrastructure.location', related='bed_id.location_id', store=True, readonly=True,
        help="Bed assigned to the patient in this encounter.")
    date_start = fields.Datetime(
        'Start Date', default=fields.Datetime.now, required=True)
    date_end = fields.Datetime('End Date')
