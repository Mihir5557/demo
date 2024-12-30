# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    timesheet_activity_id = fields.Many2one('project.timesheet.activity', "Activity")

    def action_move_entries(self):
        result = self.env['move.timesheet.entry'].create({
            'analytic_line_ids': self.ids
        })

        return {
            'name': _('Move Entries'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'move.timesheet.entry',
            'res_id': result.id,
            'target': 'new',
        }

