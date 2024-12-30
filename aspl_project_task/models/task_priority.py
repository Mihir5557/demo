# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, _


class TaskPriority(models.Model):
    _name = "task.priority"
    _description = 'Task Priority'
    _order = "sequence,id"

    sequence = fields.Integer("Sequence")
    name = fields.Char('Priority')
    color = fields.Char(string='Color', default=0)
