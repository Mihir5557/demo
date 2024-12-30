# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, _, fields


class Project(models.Model):
    _inherit = "project.project"

    project_lead_id = fields.Many2one('res.users', string='Project Lead')
    reopen_stage_id = fields.Many2one('project.task.type', string='Reopened task goes to',
                                      domain="[('project_ids', 'in', [id])]")

    def open_project_view_for_user(self):
        
        group_hr_manager = self.env.user.has_group('hr.group_hr_manager')
        if group_hr_manager:
            view_id = self.env.ref('project.edit_project').sudo()
        else:
            view_id = self.env.ref('aspl_project.edit_project_for_user').sudo()
            
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'project.project',
            'view_type':'form',
            'view_mode':'form',
            'name':_('Projects'),
            'target':'new',
            'res_id': self.id,
            'view_id': view_id.id,
        }
       