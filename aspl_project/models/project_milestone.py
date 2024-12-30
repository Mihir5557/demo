# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _

class Project(models.Model):
    _inherit = "project.milestone"

    task_count = fields.Integer("Project Tasks Count", compute="_compute_task_count")

    @api.depends('project_id')
    def _compute_task_count(self):
        for rec in self:
            task_ids = self.env['project.task'].search([('milestone_id', '=', rec.id)])
            rec.task_count = len(task_ids)

    def action_task_to_kanban(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Tasks'),
            'res_model': 'project.task',
            'view_mode': 'kanban,tree,form',
            'target': 'current',
            'domain': [('milestone_id', '=', self.id), ('project_id', '=', self.project_id.id)],
            'views': [[False, 'kanban']]
        }
