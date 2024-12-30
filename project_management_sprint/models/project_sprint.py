# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ProjectSprint(models.Model):
    _name = 'project.sprint'
    _inherit = 'mail.thread'
    _description = 'Project Sprint'

    name = fields.Char(string="Sprint Name", help="Name of the sprint")
    sprint_goal = fields.Text(string="Goal", help="Goal of the sprint")
    start_date = fields.Date(string="Start Date", help="Sprint start date")
    end_date = fields.Date(string="End Date", help="Sprint end date")
    project_id = fields.Many2one('project.project', help="Respective Project", required=True)
    state = fields.Selection(string="State",
                             selection=[('to_start', 'To start'),
                                        ('ongoing', 'Ongoing'),
                                        ('completed', 'Completed')],
                             default='to_start', help="State of the sprint")

    @api.model_create_multi
    def create(self, vals_list):
        is_project_manager = self.env.user.has_group('project.group_project_manager')
        for vals in vals_list:
            if not is_project_manager:
                project_id = self.env['project.project'].browse(vals.get('project_id'))
                if project_id.project_lead_id.id != self.env.user.id:
                    raise ValidationError('A project manager or project leader can only create a record !!!')

        return super(ProjectSprint, self).create(vals_list)

    def _check_user_permissions(self):
        if not (self.env.user.has_group('project.group_project_manager') or
                self.project_id.project_lead_id.id == self.env.user.id):
            raise ValidationError('A project manager or project leader can only update or delete a record !!!')

    def write(self, vals):
        self._check_user_permissions()
        return super(ProjectSprint, self).write(vals)

    def unlink(self):
        self._check_user_permissions()
        return super(ProjectSprint, self).unlink()

    def action_get_tasks(self):
        """ Sprint added tasks """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tasks',
            'view_mode': 'kanban',
            'res_model': 'project.task',
            'views': [[False, 'kanban'], [False, 'list'], [False, 'form']],
            'domain': [('project_id', '=', self.project_id.id),
                       ('sprint_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def action_get_backlogs(self):
        """ Tasks without any sprint """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Backlogs',
            'view_mode': 'kanban',
            'res_model': 'project.task',
            'views': [[False, 'kanban'], [False, 'list'], [False, 'form']],
            'domain': [('project_id', '=', self.project_id.id),
                       ('sprint_id', '=', False)],
            'context': "{'create': False}"
        }

    def action_get_all_tasks(self):
        """ All tasks in the project """
        return {
            'type': 'ir.actions.act_window',
            'name': 'All Tasks',
            'view_mode': 'kanban',
            'res_model': 'project.task',
            'views': [[False, 'kanban'], [False, 'list'], [False, 'form']],
            'domain': [('project_id', '=', self.project_id.id)],
            'context': "{'create': False}"
        }

    def action_start_sprint(self):
        """ Sprint state to ongoing """
        self.write({'state': 'ongoing'})

    def action_finish_sprint(self):
        """ Sprint state to completed """
        self.write({'state': 'completed'})

    def action_reset_states(self):
        """ Sprint state to to_start """
        self.write({'state': 'to_start'})
