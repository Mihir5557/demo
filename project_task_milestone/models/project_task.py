# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    milestone_id = fields.Many2one(
        "project.milestone",
        string="Milestone",
        group_expand="_read_group_milestone_ids",
        domain="[('project_id', '=', project_id)]",
    )

    @api.model
    def _read_group_milestone_ids(self, milestone_ids, domain, order=None):
        if "default_project_id" in self.env.context:
            milestone_ids = self.env["project.milestone"].search(
                [("project_id", "=", self.env.context["default_project_id"])]
            )
        return milestone_ids
