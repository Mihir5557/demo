# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    project_id = fields.Many2one('project.project', help="Respective Project")
    sprint_id = fields.Many2one('project.sprint', string="Sprint",
                                help="Sprint",
                                domain="[('project_id', '=', project_id)]",
                                context={'default_project_id': project_id})
    linked_issue = fields.Selection(string="Linked issue", selection=[
        ('is_blocked_by', 'Is blocked by')], help="Linked Issue")
    issue_task_id = fields.Many2one('project.task', string="Task",
                                    help="Task")

    @api.constrains('stage_id')
    def _check_stage_id(self):
        for rec in self:
            if rec.linked_issue:
                raise UserError(f"'{rec.name}' task is linked to another task and cannot be modified.")
