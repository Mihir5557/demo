# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProjectMilestone(models.Model):
    _inherit = "project.milestone"

    active = fields.Boolean('Active', default=True)
