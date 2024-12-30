# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import timedelta, date
import logging

_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = 'project.task'
    _order = "priority_task_sequence desc,sequence, id desc"

    code_review_comment_ids = fields.One2many('code.review.comment', 'ref_field_id', string="Code Review Comment")
    type_of_task_id = fields.Many2one('project.task.selection')
    type_of_task_color = fields.Char(string="Type of Task color", related="type_of_task_id.color", tracking=True)
    task_priority = fields.Selection(
        [('lowest', 'Lowest'), ('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('highest', 'Highest')],
        string='Priority', tracking=True)
    priority_task_id = fields.Many2one('task.priority', "Priority", tracking=True)
    priority_task_color = fields.Char(string="Priority Task color", related="priority_task_id.color")
    priority_task_sequence = fields.Integer(related="priority_task_id.sequence", store=True)
    story_points = fields.Selection(
        [('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('5', '5'), ('8', '8'), ('13', '13'), ('21', '21')],
        string='Story Points', tracking=True)
    last_update = fields.Char("Last Update", compute='_compute_last_update')
    last_update_label = fields.Char(compute='_compute_last_update_label')

    def _compute_last_update_label(self):
        self = self.sudo()
        today = date.today()
        yesterday = today - timedelta(days=1)

        for rec in self:
            if rec.timesheet_ids:
                timesheet_list = []
                for timesheet in rec.timesheet_ids:
                    if timesheet.date and timesheet.employee_id:
                        if timesheet.date == today:
                            label_date = "Today"
                        elif timesheet.date == yesterday:
                            label_date = "Yesterday"
                        else:
                            label_date = timesheet.date.strftime("%d/%m/%y")

                        label_name = ''.join(name[0] for name in filter(None, timesheet.employee_id.name.split(" ")))
                        last_update_label = f"{label_date}[{label_name[:2]}]"
                        timesheet_list.append(last_update_label)

                rec.last_update_label = timesheet_list[0] if timesheet_list else False
            else:
                rec.last_update_label = False

    def _compute_last_update(self):
        for rec in self:
            if rec.timesheet_ids:
                rec.last_update = next((timesheet.name[:100] for timesheet in rec.timesheet_ids if timesheet.name),False)
            else:
                rec.last_update = False
