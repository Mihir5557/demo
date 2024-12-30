# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class ProjectTimesheetActivity(models.Model):
    _name = "project.timesheet.activity"
    _description = "Project Timesheet Activity"

    name = fields.Char("Activity")
