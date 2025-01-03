# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.http import request

from odoo import models, fields, api, _


# Employee family information
class EmployeeAppraisal(models.Model):
    _name = "employee.appraisal"
    _description = "Employee Appraisal"
    _order = "create_date desc"

    appraisal_date = fields.Date('Appraisal Date', default=datetime.today().date())  # default=_default_appraisal_dat
    employee_id = fields.Many2one('hr.employee', string="Employee")
    months = fields.Integer()
    document = fields.Binary()
    document_name = fields.Char('Attachment Name')
    meeting_document = fields.Binary()
    meeting_document_name = fields.Char('Meeting Document')
    new_ctc = fields.Integer("New CTC")
    old_ctc = fields.Integer("Old CTC")
    percentage_hike = fields.Integer("Hike %", compute="_compute_hike")
    appraisal_note = fields.Text('Appraisal Note')
    status = fields.Selection(string='Status', selection=[('lock', 'Lock'),
                                                          ('unlock', 'Unlock'),
                                                          ], default='lock')
    accept_token = fields.Char('Accept Token')
    reject_token = fields.Char('Reject Token')

    def generate_employee_letter(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'employee.letter.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'name': _('Employee Letter'),
            'target': 'new',
            'context': {'appraisal_id': self.id, 'employee_id': [
                self.env.context.get('params').get('id') if self.env.context.get('params') else self.env.context.get(
                    'params')]},
        }

    def unlink(self):
        for rec in self:
            employee_obj = rec.employee_id
            appraisal_date = rec.appraisal_date.strftime("%d/%m/%Y")
            res = super(EmployeeAppraisal, self).unlink()

            # Add Log Note
            employee_obj.message_post(body="Appraisal Document deleted - %s" % appraisal_date)

        return res

    @api.onchange('appraisal_date')
    def on_change_appraisal_date(self):
        for record in self:
            previous_dates = [i.appraisal_date for i in record.employee_id.appraisal_ids] if record.employee_id else []
            old_ctc_list = [i.new_ctc for i in record.employee_id.appraisal_ids] if record.employee_id else []
            len_app = len(record.employee_id.appraisal_ids) if record.employee_id else 0

            num_months = 0

            if len_app > 1 and record.appraisal_date and previous_dates:
                num_months = (record.appraisal_date.year - previous_dates[0].year) * 12 + (
                        record.appraisal_date.month - previous_dates[0].month)
                record.months = num_months
                record.old_ctc = old_ctc_list[0] if old_ctc_list else 0
            elif record.appraisal_date and record.employee_id and record.employee_id.join_date:
                num_months = (record.appraisal_date.year - record.employee_id.join_date.year) * 12 + (
                        record.appraisal_date.month - record.employee_id.join_date.month)
                record.months = num_months
                record.old_ctc = old_ctc_list[0] if old_ctc_list else 0
            else:
                record.months = num_months
                record.old_ctc = old_ctc_list[0] if old_ctc_list else 0

    @api.depends('new_ctc', 'old_ctc')
    def _compute_hike(self):
        for record in self:
            if record.old_ctc and record.new_ctc:
                record.percentage_hike = (record.new_ctc - record.old_ctc) / (record.old_ctc / 100)
            else:
                record.percentage_hike = 0
