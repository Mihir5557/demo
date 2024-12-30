# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProjectProject(models.Model):
    _inherit = 'project.project'

    task_type_ids = fields.One2many('project.task.selection', 'project_id', 'Task Type')

    @api.model_create_multi
    def create(self, vals_list):
        result = super(ProjectProject, self).create(vals_list)

        selections = [
            {'name': 'Task', 'color': 'green'},
            {'name': 'Bug', 'color': 'red'},
            {'name': 'Support', 'color': '#5A5A5A'}
        ]

        task_selection_data = [
            {'name': selection['name'], 'color': selection['color'], 'project_id': result.id}
            for selection in selections
        ]

        self.env['project.task.selection'].create(task_selection_data)
        return result
