# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import time
from datetime import date, datetime
from odoo.exceptions import ValidationError

from odoo import models, fields, api, _
from ..common.validation import Validation
from ..constant.constant import Constant

_logger = logging.getLogger(__name__)


class ReportingHistory(models.Model):
    _name = 'reporting.history'
    _description = 'reporting.history'
    _order = "effective_from desc"

    employee_id = fields.Many2one('hr.employee', 'Employee')
    category_type = fields.Char('Category Type', default='Reporting', readonly=True)
    parent_id = fields.Many2one('hr.employee', 'Reporting To', required=True)
    effective_from = fields.Date('Effective From', required=True)
    effective_to = fields.Date('Effective To')
    current_reporting = fields.Boolean('Current Reporting', default=True)

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            emp_id = val.get('employee_id')
            effective_from = val.get('effective_from')
            parent_id = val.get('parent_id')
            hr_employee_data = self.env['hr.employee'].browse(emp_id)
            parent_id_data = self.env['hr.employee'].browse(parent_id)
            position_history_data_list = hr_employee_data.position_reporting

            if position_history_data_list:
                effective_date_data = []
                for position_history in position_history_data_list:
                    effective_date_data.append(position_history.effective_from)

                if effective_date_data:
                    effective_date = max(effective_date_data)
                    today = datetime.today()
                    time = datetime.min.time()
                    formatted_effective_from = datetime.strptime(effective_from, '%Y-%m-%d')
                    formatted_effective_date = datetime.combine(effective_date, time)
                    if formatted_effective_from > formatted_effective_date and formatted_effective_from <= today:
                        hr_employee_data.write({'parent_id': parent_id_data.id})
                        hr_employee_data.write({'coach_id': parent_id_data.id})

            else:
                hr_employee_data.write({'parent_id': parent_id_data.id})
                hr_employee_data.write({'coach_id': parent_id_data.id})

        return super(ReportingHistory, self).create(vals)

    # Constraints for effective_to validation
    @api.constrains('effective_from', 'effective_to')
    def _check_dates_constraints(self):
        for record in self:
            if record.effective_from and record.effective_to:
                flag = Validation.check_date(record.effective_from, record.effective_to)
                if not flag:
                    raise ValidationError(Constant.INVALID_REPORTING_DATE)
            return True
