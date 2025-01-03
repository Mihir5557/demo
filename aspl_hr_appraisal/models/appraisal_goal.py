# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, api, models
from odoo.exceptions import ValidationError


class HrAppraisalGoal(models.Model):
    _name = "appraisal.goal"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Appraisal Goal"

    name = fields.Char(required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee",
                                  default=lambda self: self.env.user.employee_id, required=True)
    manager_id = fields.Many2one('hr.employee', string="Manager", required=True)
    manager_user_id = fields.Many2one('res.users', related='manager_id.user_id')
    description = fields.Html(string='Description')
    deadline = fields.Date(string='Deadline')
    notes = fields.Html(string="Description", help="The content of this description is not visible by the Employee.")
    show_attachments = fields.Boolean(string="Show Attachments", default=False)
    attachment_file = fields.Binary(string="Attachment")
    attachment_filename = fields.Char(string="Attachment Filename")
    progression = fields.Selection(selection=[
        ('0', '0 %'),
        ('25', '25 %'),
        ('50', '50 %'),
        ('75', '75 %'),
        ('100', '100 %')
    ], string="Progress", tracking=True, readonly=True)
    is_manager = fields.Boolean(string="Is Manager", compute="_compute_is_manager")

    @api.constrains('progression')
    def _check_progression_edit(self):
        for record in self:
            if self.env.user == record.employee_id.user_id and 'aspl_hr_appraisal.group_hr_appraisal_user':
                if record.progression > '0 %':
                    raise ValidationError("Employees cannot edit the goal progression percentage.")

    def _compute_is_manager(self):
        for record in self:
            record.is_manager = self.env.user.has_group('hr_appraisal.group_hr_appraisal_user')

    def action_confirm(self):
        for record in self:
            if self.env.user == record.employee_id.user_id:
                raise ValidationError("Only the manager can mark this goal as done.")
        self.write({'progression': '100'})
