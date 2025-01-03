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
class CompanyHistory(models.Model):
    _name = "company.history"
    _description = "Employee company history"
    _order = "effective_from desc"

    employee_id = fields.Many2one('hr.employee', 'Employee')
    category_type = fields.Char('Category Type', default='company', readonly=True)

    employment_type = fields.Selection([
        ('permanent_employee', 'Permanent Employee'),
        ('consultant_aspire', 'Consultant Aspire'),
        ('trainee', 'Trainee'),
        ('temporary_employee', 'Temporary Employee'),
        ('client', 'Client'),
        ('consultant_other', 'Consultant Other')
    ], 'Employment Type', help="Select Employment Type")
    company_id = fields.Many2one('res.company', 'Company Name')
    company_employment_type = fields.Many2one('company.employment.type', 'Employment type',
                                              domain="[('company_id','=',company_id)]")

    effective_from = fields.Date('Effective From', required=True, default=datetime.today().date())
    effective_to = fields.Date('Effective To')
    current_company = fields.Boolean('Current company', default=True)
    employee_no = fields.Char("Employee No")

    def write(self, vals):
        temp_higher_date = ""
        for compnay_history_id in self:
            if 'employee_id' in vals:
                employee_data = self.env['hr.employee'].search([('id', '=', vals['employee_id'])])

                if employee_data:
                    higher_employement_date = employee_data.position_company.sorted(
                        key=lambda company_postion_record_id: company_postion_record_id.effective_from, reverse=True
                    )
                    if higher_employement_date:
                        higher_employement_date = higher_employement_date[0]
                        if temp_higher_date != "" and compnay_history_id.effective_from >= temp_higher_date or temp_higher_date == "" and compnay_history_id.effective_from >= higher_employement_date.effective_from:
                            employee_data.write({'employee_no': compnay_history_id.employee_no,
                                                 'employee_no_type': compnay_history_id.company_employment_type.company_employment_type,
                                                 'company_id': compnay_history_id.company_id.id})
                            temp_higher_date = compnay_history_id.effective_from
                    else:
                        employee_data.write({'employee_no': compnay_history_id.employee_no,
                                             'employee_no_type': compnay_history_id.company_employment_type.company_employment_type,
                                             'company_id': compnay_history_id.company_id.id})
            else:
                emp_dict = {}
                higher_employement_date = self.employee_id.position_company.sorted(
                    key=lambda company_postion_record_id: company_postion_record_id.effective_from, reverse=True
                )
                if higher_employement_date:
                    higher_employement_date = higher_employement_date[0]
                    if compnay_history_id.effective_from >= higher_employement_date.effective_from:
                        if 'company_employment_type' in vals and vals['company_employment_type']:
                            company_employment_type = self.env['company.employment.type'].browse(
                                vals['company_employment_type'])
                            emp_dict['employee_no_type'] = company_employment_type.company_employment_type

                        if 'employee_no' in vals and vals['employee_no']:
                            emp_dict['employee_no'] = vals['employee_no']

                        if 'company_id' in vals and vals['company_id']:
                            emp_dict['company_id'] = vals['company_id']

                        if emp_dict:
                            compnay_history_id.employee_id.write(emp_dict)
        return super(CompanyHistory, self).write(vals)

    def create(self, vals):
        res = super(CompanyHistory, self).create(vals)
        emp_dict = {}
        higher_employement_date = res.employee_id.position_company.sorted(
            key=lambda company_postion_record_id: company_postion_record_id.effective_from, reverse=True
        )
        if higher_employement_date:
            higher_employement_date = higher_employement_date[0]
            if self.effective_from >= higher_employement_date.effective_from:
                if res.company_employment_type:
                    emp_dict['employee_no_type'] = res.company_employment_type.company_employment_type
                if res.employee_no:
                    emp_dict['employee_no'] = res.employee_no
                if res.company_id and res.company_id.id != res.employee_id.company_id.id:
                    emp_dict['company_id'] = res.company_id.id
                if emp_dict:
                    res.employee_id.write(emp_dict)
        return res

    # Constraints for effective_to validation
    @api.constrains('effective_from', 'effective_to')
    def _check_dates_constraints(self):
        for rec in self:
            if rec.effective_from and rec.effective_to and (rec.effective_to != rec.effective_from):
                flag = Validation.check_date(rec.effective_from, rec.effective_to)
                if not flag:
                    raise ValidationError(Constant.INVALID_COMPANY_DATE)
        return True

    def next_by_code(self, sequence_code, sequence_date=None):
        self.env['ir.sequence'].check_access_rights('read')
        seq_ids = self.env['ir.sequence'].search([('code', '=', sequence_code)])
        seq_id = seq_ids[0]
        return seq_id._next(sequence_date=sequence_date)

    def _get_previous_by_code(self, sequence):
        employee_next_no = sequence.get_next_char(sequence.number_next_actual)
        next_number_actual_count = int(sequence.number_next_actual) - 1
        employee_no = int(employee_next_no) - 2
        check_employee_no = self.env['company.history'].search([('employee_no', 'ilike', str(employee_no))])
        if check_employee_no:
            raise ValidationError(_("You are not able to perform Previous step."))
        else:
            sequence.write({'number_next_actual': next_number_actual_count})
            return employee_no

    def generate_sequence_employee(self):
        sequence = self.env['ir.sequence'].search([('name', '=', self.company_employment_type.company_employment_type),
                                                   ('company_id', '=', self.company_id.id)])
        if sequence:
            sequence_code = sequence.code
            self.employee_no = self.next_by_code(sequence_code)
        else:
            raise ValidationError(_("Make sure sequence created for this combination."))
        return self

    def get_previous_sequence_employee(self):
        sequence = self.env['ir.sequence'].search([('name', '=', self.company_employment_type.company_employment_type),
                                                   ('company_id', '=', self.company_id.id)])
        self.employee_no = self._get_previous_by_code(sequence)
        return self
