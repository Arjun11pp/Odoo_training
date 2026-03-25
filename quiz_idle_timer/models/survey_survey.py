# -*- coding: utf-8 -*-

from odoo import fields, models,api

class SurveySurvey(models.Model):
    """ Inherits survey.survey Quiz Idle Timer """

    _inherit = 'survey.survey'

    idle_timer=fields.Char(string='Idle Timer')

