# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ReportProjectTaskUser(models.Model):
    _inherit = "report.project.task.user"

    sprint_id = fields.Many2one('project.sprint', string="Sprint", readonly=True)
