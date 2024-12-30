# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    def action_get_sprint(self):
        """ Getting sprint inside the project """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sprints',
            'view_mode': 'list,form',
            'res_model': 'project.sprint',
            'context': {'default_project_id': self.id},
            'domain': [('project_id', '=', self.id)],
        }
