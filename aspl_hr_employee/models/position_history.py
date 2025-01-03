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


# Employee position history
class DesignationHistory(models.Model):
    _name = "designation.history"
    _description = "Employee designation history"
    _order = "effective_from desc"

    employee_id = fields.Many2one('hr.employee', 'Employee')
    category_type = fields.Char('Category Type', default='Designation', readonly=True)
    job_id = fields.Many2one('hr.job', 'Job Title', required=True)
    effective_from = fields.Date('Effective From', required=True)
    effective_to = fields.Date('Effective To')
    current_designation = fields.Boolean('Current Designation', default=True)
    contract_id = fields.Many2one('hr.contract')

    # Constraints for effective_to validation
    @api.constrains('effective_from', 'effective_to')
    def _check_dates_constraints(self):
        for record in self:
            if record.effective_from and record.effective_to:
                flag = Validation.check_date(record.effective_from, record.effective_to)
                if not flag:
                    raise ValidationError(Constant.INVALID_DESIGNATION_DATE)


class LocationHistory(models.Model):
    _name = "location.history"
    _description = "Employee location history"
    _order = "effective_from desc"

    employee_id = fields.Many2one('hr.employee', 'Employee')
    category_type = fields.Char('Category Type', default='Location', readonly=True)
    location_street = fields.Char('Street', required=True)
    location_city = fields.Char('City', size=30, help='City max size is 30', required=True)
    location_pcode = fields.Char('Pin code', size=6, help='Pin Code max size is 6', required=True)
    location_id = fields.Many2one('res.country.state', 'State', required=True)
    location_county = fields.Many2one('res.country', 'Country', required=True)
    effective_from = fields.Date('Effective From', required=True)
    effective_to = fields.Date('Effective To')
    current_location = fields.Boolean('Current Location', default=True)

    # Constraints for effective_to validation
    @api.constrains('effective_from', 'effective_to')
    def _check_dates_constraints(self):
        for record in self:
            if record.effective_from and record.effective_to:
                flag = Validation.check_date(record.effective_from, record.effective_to)
                if not flag:
                    raise ValidationError(Constant.INVALID_LOCATION_DATE)


class DepartmentHistory(models.Model):
    _name = "department.history"
    _description = "Employee Department history"
    _order = "effective_from desc"

    employee_id = fields.Many2one('hr.employee', 'Employee')
    category_type = fields.Char('Category Type', default='Department', readonly=True)
    department_id = fields.Many2one('hr.department', 'Department', required=True)
    effective_from = fields.Date('Effective From', required=True)
    effective_to = fields.Date('Effective To')
    current_department = fields.Boolean('Current Department', default=True)

    # Constraints for effective_to validation
    @api.constrains('effective_from', 'effective_to')
    def _check_dates_constraints(self):
        for record in self:
            if record.effective_from and record.effective_to:
                flag = Validation.check_date(record.effective_from, record.effective_to)
                if not flag:
                    raise ValidationError(Constant.INVALID_DEPARTMENT_DATE)
