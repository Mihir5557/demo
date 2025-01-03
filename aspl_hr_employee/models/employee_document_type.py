# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class EmployeeDocumentType(models.Model):
    _name = "employee.document.type"
    _description = "Employee Document Type"

    name = fields.Char(string="Name")
    document_type = fields.Many2many("employee.document.category", string="Document Type")
