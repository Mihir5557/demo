# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class EmployeeDocumentCategory(models.Model):
    _name = "employee.document.category"
    _description = "Employee Document category"

    name = fields.Char(string="Name")
