# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, tools


class ProjectSprintReport(models.Model):
    _name = 'project.sprint.report'
    _description = 'Project Sprint Report'
    _auto = False

    sprint_id = fields.Many2one('project.sprint', string="Sprint")
    project_id = fields.Many2one('project.project', readonly=True)
    display_project_id = fields.Many2one('project.project', readonly=True)
    stage_id = fields.Many2one('project.task.type', string="Stage")
    task_id = fields.Many2one('project.task', readonly=True)
    date = fields.Datetime('Date', readonly=True)
    user_ids = fields.Many2many('res.users', relation='project_task_user_rel', column1='task_id', column2='user_id',
                                string='Assignees', readonly=True)
    date_assign = fields.Datetime(string='Assignment Date', readonly=True)
    date_deadline = fields.Date(string='Deadline', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True)
    nb_tasks = fields.Integer('# of Tasks', readonly=True, aggregator="sum")
    date_group_by = fields.Selection(
        (
            ('day', 'By Day'),
            ('month', 'By Month'),
            ('quarter', 'By quarter'),
            ('year', 'By Year')
        ), string="Date Group By", readonly=True)

    def init(self):
        """ Project Sprint Report """

        tools.drop_view_if_exists(self._cr, 'project_sprint_report')
        self._cr.execute("""
CREATE OR REPLACE VIEW project_sprint_report AS (
    WITH all_moves_stage_task AS (
        -- Compute all previous stages in tracking values
        SELECT pt.project_id AS project_id,  -- Alias project_id here
               pt.sprint_id AS sprint_id,
               pt.id AS task_id,
               COALESCE(LAG(mm.date) OVER (PARTITION BY mm.res_id ORDER BY mm.id), pt.create_date) AS date_begin,
               mm.date AS date_end,
               mtv.old_value_integer AS stage_id,
               pt.date_assign,
               pt.date_deadline,
               pt.partner_id
          FROM project_task pt
          JOIN mail_message mm ON mm.res_id = pt.id
                              AND mm.message_type = 'notification'
                              AND mm.model = 'project.task'
          JOIN mail_tracking_value mtv ON mm.id = mtv.mail_message_id
          JOIN ir_model_fields imf ON mtv.field_id = imf.id
                                  AND imf.model = 'project.task'
                                  AND imf.name = 'stage_id'
          JOIN project_task_type_rel pttr ON pttr.type_id = mtv.old_value_integer
                                           AND pt.project_id = pttr.project_id
         WHERE pt.active AND pt.sprint_id IS NOT NULL

        -- Compute the last reached stage
        UNION ALL

        SELECT pt.project_id AS project_id,  -- Alias project_id here
               pt.sprint_id AS sprint_id,
               pt.id AS task_id,
               COALESCE(md.date, pt.create_date) AS date_begin,
               (CURRENT_DATE + interval '1 month')::date AS date_end,
               pt.stage_id AS stage_id,
               pt.date_assign AS date_assign,
               pt.date_deadline AS date_deadline,
               pt.partner_id AS partner_id
          FROM project_task pt
          LEFT JOIN LATERAL (SELECT mm.date
                              FROM mail_message mm
                              JOIN mail_tracking_value mtv ON mm.id = mtv.mail_message_id
                              JOIN ir_model_fields imf ON mtv.field_id = imf.id
                                                      AND imf.model = 'project.task'
                                                      AND imf.name = 'stage_id'
                             WHERE mm.res_id = pt.id
                               AND mm.message_type = 'notification'
                               AND mm.model = 'project.task'
                          ORDER BY mm.id DESC
                             FETCH FIRST ROW ONLY) md ON TRUE
         WHERE pt.active AND pt.sprint_id IS NOT NULL
    )
    -- Main Query with Joins
    SELECT t.*,
           ps.name AS sprint_name
      FROM (
        SELECT (task_id*10^7 + 10^6 + to_char(d, 'YYMMDD')::integer)::bigint AS id,
               t.project_id,  -- Reference project_id here
               t.sprint_id,
               t.task_id,
               t.stage_id,
               d AS date,
               t.date_assign,
               t.date_deadline,
               t.partner_id,
               'day' AS date_group_by,
               1 AS nb_tasks
          FROM all_moves_stage_task t
          JOIN LATERAL generate_series(t.date_begin, t.date_end - interval '1 day', '1 day') d ON TRUE

        UNION ALL

        SELECT (task_id*10^7 + 2*10^6 + to_char(d, 'YYMMDD')::integer)::bigint AS id,
               t.project_id,  -- Reference project_id here
               t.sprint_id,
               t.task_id,
               t.stage_id,
               date_trunc('week', d) AS date,
               t.date_assign,
               t.date_deadline,
               t.partner_id,
               'week' AS date_group_by,
               1 AS nb_tasks
          FROM all_moves_stage_task t
          JOIN LATERAL generate_series(t.date_begin, t.date_end, '1 week') d ON TRUE
         WHERE date_trunc('week', t.date_begin) <= date_trunc('week', d)
           AND date_trunc('week', t.date_end) > date_trunc('week', d)

        UNION ALL

        SELECT (task_id*10^7 + 3*10^6 + to_char(d, 'YYMMDD')::integer)::bigint AS id,
               t.project_id,  -- Reference project_id here
               t.sprint_id,
               t.task_id,
               t.stage_id,
               date_trunc('month', d) AS date,
               t.date_assign,
               t.date_deadline,
               t.partner_id,
               'month' AS date_group_by,
               1 AS nb_tasks
          FROM all_moves_stage_task t
          JOIN LATERAL generate_series(t.date_begin, t.date_end, '1 month') d ON TRUE
         WHERE date_trunc('month', t.date_begin) <= date_trunc('month', d)
           AND date_trunc('month', t.date_end) > date_trunc('month', d)

        UNION ALL

        SELECT (task_id*10^7 + 4*10^6 + to_char(d, 'YYMMDD')::integer)::bigint AS id,
               t.project_id,  -- Reference project_id here
               t.sprint_id,
               t.task_id,
               t.stage_id,
               date_trunc('quarter', d) AS date,
               t.date_assign,
               t.date_deadline,
               t.partner_id,
               'quarter' AS date_group_by,
               1 AS nb_tasks
          FROM all_moves_stage_task t
          JOIN LATERAL generate_series(t.date_begin, t.date_end, '3 month') d ON TRUE
         WHERE date_trunc('quarter', t.date_begin) <= date_trunc('quarter', d)
           AND date_trunc('quarter', t.date_end) > date_trunc('quarter', d)

        UNION ALL

        SELECT (task_id*10^7 + 5*10^6 + to_char(d, 'YYMMDD')::integer)::bigint AS id,
               t.project_id,  -- Reference project_id here
               t.sprint_id,
               t.task_id,
               t.stage_id,
               date_trunc('year', d) AS date,
               t.date_assign,
               t.date_deadline,
               t.partner_id,
               'year' AS date_group_by,
               1 AS nb_tasks
          FROM all_moves_stage_task t
          JOIN LATERAL generate_series(t.date_begin, t.date_end, '1 year') d ON TRUE
         WHERE date_trunc('year', t.date_begin) <= date_trunc('year', d)
           AND date_trunc('year', t.date_end) > date_trunc('year', d)
    ) t
    JOIN project_sprint ps ON ps.id = t.sprint_id
)
""")
