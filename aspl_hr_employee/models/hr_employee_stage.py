# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class HrEmployeeStage(models.Model):
    _name = "hr.employee.stage"
    _description = "HR Employee Stage"
    _rec_name = "name"

    name = fields.Char(string="Name")
    field_name = fields.Char(string="Field Name")
