# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class CodeReviewCategory(models.Model):
    _name = 'code.review.category'
    _description = 'Code Review Category'
    _rec_name = 'name'

    name = fields.Char('Name')
