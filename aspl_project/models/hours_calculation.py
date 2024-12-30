import logging

from odoo import models, _, fields, api

_logger = logging.getLogger(__name__)


class Task(models.Model):
    _name = "project.task"
    _inherit = "project.task"

    effective_hours = fields.Float("Hours Spent", compute='_compute_effective_hours', compute_sudo=True, store=True, help="Time spent on this task, excluding its sub-tasks.")
    reopen_count = fields.Integer(string="Reopen Count")
    is_closed = fields.Boolean(string='Closing Stage')
    display_project_id = fields.Many2one('project.project')
    planned_hours = fields.Float(string="Initially Planned Hours")

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        for rec in self:
            rec.is_closed = True if rec.stage_id.is_closed else False

    def action_reopen(self):
        try:
            if self.stage_id != self.project_id.reopen_stage_id:
                self.stage_id = self.project_id.reopen_stage_id
                self.reopen_count += 1
        except Exception as e:
            _logger.error('Something is wrong')
            _logger.error(str(e))

    def interchange_time_entry_task(self):

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'timesheet.task.change',
            'view_type':'form',
            'view_mode':'form',
            'name':_('Timesheet Entry Task Change'),
            'target':'new',
            'context': {'task_id':self.id},
        }
