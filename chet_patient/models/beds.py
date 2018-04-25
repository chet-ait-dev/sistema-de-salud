# -*- coding: utf-8 -*-

from odoo import fields, models


class InfrastructureBed(models.Model):
    _name = 'infrastructure.bed'

    name = fields.Char('Bed Name')
    code = fields.Char()
    # TODO: Add a constraint for uniqueness of code
