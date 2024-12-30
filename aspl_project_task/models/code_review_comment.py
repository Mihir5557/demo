# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class CodeReviewComment(models.Model):
    _name = 'code.review.comment'
    _description = 'Code Review Comment'

    employee_id = fields.Many2one('hr.employee', string="Employee", domain=[('with_organization', "=", True)])
    category_id = fields.Many2one('code.review.category', 'Category')
    severity = fields.Selection(
        [('Minor', 'Minor'), ('Major', 'Major'), ('Critical', 'Critical'), ('Blocker', 'Blocker')], string="Severity")
    desc = fields.Text('Description')
    ref_field_id = fields.Many2one('project.task')
