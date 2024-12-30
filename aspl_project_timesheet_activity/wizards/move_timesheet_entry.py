# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class MoveTimesheetEntry(models.TransientModel):
    _name = 'move.timesheet.entry'
    _description = 'Move Timesheet Entry'

    def get_project_domain(self):
        user = self.env.user
        return ['|', '|',
                ('privacy_visibility', '!=', 'followers'),
                ('message_partner_ids', 'in', [user.partner_id.id]), ('members_ids', 'in', [user.id])
                ]

    project_id = fields.Many2one('project.project', string='Project', domain=get_project_domain)
    task_id = fields.Many2one('project.task', string="Task")
    analytic_line_ids = fields.Many2many('account.analytic.line')

    def action_move_entries(self):
        for rec in self.analytic_line_ids:
            if rec.sheet_id.company_id:
                query = "Update account_analytic_line set project_id = %s, task_id = %s, company_id = %s WHERE id = %s"
                self._cr.execute(query, (self.project_id.id, self.task_id.id, rec.sheet_id.company_id.id, rec.id))
            else:
                query = "Update account_analytic_line set project_id = %s, task_id = %s WHERE id = %s"
                self._cr.execute(query, (self.project_id.id, self.task_id.id, rec.id))
