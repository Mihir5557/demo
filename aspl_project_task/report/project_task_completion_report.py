# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, tools


class ProjectTaskCompletionReport(models.Model):
    _name = 'project.task.completion.report'
    _description = 'Project Task Completion Report'
    _auto = False

    employee_id = fields.Many2one('hr.employee', string='Employee')
    project_task_id = fields.Many2one('project.task', string='Project Task')
    project_id = fields.Many2one('project.project', string='Project')
    task_completion_date = fields.Date(string='Task Completion Date')
    planned_hours = fields.Float(string="Initially Planned Hours")
    spent_time = fields.Float(string="Time Spent")

    def init(self):
        """ Task Completion Report """
        tools.drop_view_if_exists(self._cr, 'project_task_completion_report')
        self._cr.execute("""
                            CREATE OR REPLACE VIEW project_task_completion_report AS (
                                select row_number() OVER () as id, aal.task_id as project_task_id, max(aal.date) as task_completion_date, aal.project_id as project_id, aal.employee_id as employee_id, pt.allocated_hours as planned_hours, SUM(aal.unit_amount) as spent_time from account_analytic_line aal  JOIN project_task pt ON aal.task_id = pt.id where task_id in (
                                    select id from project_task where stage_id in (
                                        select id from project_task_type)) group by aal.task_id, aal.project_id, aal.employee_id, pt.allocated_hours
                            )""")
