# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    @api.depends('child_ids', 'child_ids.child_all_count')
    def _compute_subordinates(self):
        for employee in self:
            employee.subordinate_ids = employee._get_subordinates()
            emp_ids = self.env['hr.employee'].browse(employee.subordinate_ids.ids).filtered(lambda x: x.with_organization)
            employee.child_all_count = len(emp_ids)
