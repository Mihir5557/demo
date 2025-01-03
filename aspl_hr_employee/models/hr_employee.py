# -*- coding: utf-8 -*-
import calendar
import logging
import math
import numpy as np
import traceback
from datetime import datetime, date
from dateutil import parser
from dateutil.relativedelta import relativedelta
from odoo.addons.web.controllers.dataset import DataSet
from odoo.api import call_kw
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.http import request
from odoo.models import check_method_name

from odoo import models, fields, api, _
from ..common.validation import Validation
from ..constant.constant import Constant

_logger = logging.getLogger(__name__)

RELATION = [
    ('husband', 'Husband'),
    ('wife', 'Wife'),
    ('daughter', 'Daughter'),
    ('son', 'Son'),
    ('brother', 'Brother'),
    ('sister', 'Sister'),
    ('mother', 'Mother'),
    ('father', 'Father'),
]

SEPARATION_MODE = [
    ('awol', 'ABSENT W/O LEAVE'),
    ('contract_expire', 'CONTRACT EXPIRE'),
    ('absconding', 'ABSCONDING'),
    ('expired', 'EXPIRED'),
    ('others', 'OTHERS'),
    ('resigned', 'RESIGNED'),
    ('retired', 'RETIRED'),
    ('sick', 'SICK'),
    ('terminated', 'TERMINATED'),
    ('transferred', 'TRANSFERRED'),
]

EMPLOYMENT_TYPE = [
    ('permanent_employee', 'Permanent Employee'),
    ('temporary_employee', 'Temporary Employee'),
    ('trainee', 'Trainee'),
    ('consultant', 'Consultant'),
]


class Employee(models.Model):
    _inherit = 'hr.employee'

    # Employee joining details
    company_id = fields.Many2one('res.company', required=False)
    state_name = fields.Char("State Name", compute="_state_name")
    trainee_no = fields.Char("Trainee Code", readonly=True, tracking=True)
    join_training_date = fields.Date('Training start date', tracking=True)
    training_period = fields.Integer('Training Period', help='Enter months', default="3", tracking=True)
    training_end_date = fields.Date(string="Training End Date", tracking=True)
    join_date = fields.Date('Join Date', tracking=True)
    probation_period = fields.Integer('Probation Period', help="Enter months", default="3", tracking=True)
    probation_end_date = fields.Date('Probation End Date', tracking=True)
    confirm_date = fields.Date('Confirmed Date', tracking=True)
    notice_period = fields.Integer('Notice Period', help="Enter months", default="3", tracking=True)
    appraisal_date = fields.Date('Appraisal Due On', tracking=True)
    bond_start_date = fields.Date('Bond Start Date', tracking=True)
    bond_period = fields.Integer('Bond Period', help="Enter months", default="24", tracking=True)
    bond_end_date = fields.Date('Bond End Date', tracking=True)
    address_home_id = fields.Many2one(
        'res.partner', 'Address',
        help='Enter here the private address of the employee, not the one linked to your company.',
        groups="hr.group_hr_user", tracking=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    # When add or modifiey "emp_state" Field then Same Modification Aplly in "hr.employee.stage" Model, But if not iffective on Hr Letter then don't need to Modification of "hr.employee.stage" Model...
    emp_state = fields.Selection(
        [('new', 'New'), ('training', 'Training'), ('probation', 'Probation'), ('confirmed', 'Confirmed'),
         ('on_notice', 'On Notice Period'), ('left', 'Left Organization')], 'Status', readonly=True, default='new',
        tracking=True)

    # Employee Number
    employee_type_edit = fields.Boolean('Employee Type Edit')
    employee_no_type = fields.Selection([
        ('permanent_employee', 'Permanent Employee'),
        ('consultant_aspire', 'Consultant Aspire'),
        ('trainee', 'Trainee'),
        ('temporary_employee', 'Temporary Employee'),
        ('client', 'Client'),
        ('consultant_other', 'Consultant Other')
    ], 'Employment Type', help="Select Employment Type", tracking=True)

    # Need to add compute after creating employee from Odoo 9
    employee_no = fields.Char("Employee No", store=True, readonly=True)  # employment_type Moved to position history
    v9_employee_no = fields.Char("V9 Employee No", readonly=True)
    # Personal Details
    marriage_date = fields.Date(string='Marriage Date', tracking=True, groups="hr.group_hr_user")
    father = fields.Char(string='Father')
    spouse = fields.Char(string='Spouse')
    religion = fields.Char(string='Religion', tracking=True)
    international_employee = fields.Boolean(string='International Employee', tracking=True)
    physically_challenged = fields.Boolean('Physically Challenged', tracking=True)
    blood_group = fields.Selection(
        [('o+', 'O+'),
         ('o-', 'O-'),
         ('a+', 'A+'),
         ('a-', 'A-'),
         ('b+', 'B+'),
         ('b-', 'B-'),
         ('ab+', 'AB+'),
         ('ab-', 'AB-')], string='Blood Group', tracking=True)
    skype_id = fields.Char(string='Skype Id', size=30)
    isPresentAddSameAsPermanent = fields.Boolean(string='Same as Permanent Address')
    personal_email = fields.Char(string='Personal Email', size=240, required=True, tracking=True)
    # Experience fields
    actual_experience = fields.Char(compute='_get_actual_experience', string='Actual Experience')
    relative_experience = fields.Char(compute='_get_relative_experience', string='Relative Experience')
    experience_graduation = fields.Char(compute='_get_experience_graduation',
                                        string='Experience From Graduation')
    color = fields.Integer(string='Color Index')

    # Employee Address
    pre_street = fields.Char('Present Street', tracking=True)
    pre_landmark = fields.Char('Present Landmark', tracking=True)
    pre_city = fields.Char('Present City', size=30, help='City max size is 30', tracking=True)
    pre_pcode = fields.Char('Present Pin code', size=6, help='Pincode max size is 6', tracking=True)
    pre_state_id = fields.Many2one('res.country.state', 'Present State', tracking=True)
    pre_county_id = fields.Many2one('res.country', 'Present Country', tracking=True)
    pre_phone1 = fields.Char('Present Mobile No', tracking=True)
    pre_phone2 = fields.Char('Present Phone No', tracking=True)
    per_street = fields.Char('Permanent Street', required=True, tracking=True)
    per_landmark = fields.Char('Permanent Landmark', tracking=True)
    per_city = fields.Char('Permanent City', size=30, help="City max size is 30", required=True, tracking=True)
    per_pcode = fields.Char('Permanent Pin code', size=6, help='Pincode max size is 6', required=True, tracking=True)
    per_state_id = fields.Many2one('res.country.state', 'Permanent State', required=True, tracking=True)
    per_county_id = fields.Many2one('res.country', 'Permanent Country', required=True, tracking=True)
    per_phone1 = fields.Char('Permanent Mobile No', tracking=True)
    per_phone2 = fields.Char('Permanent Phone No', tracking=True)

    # Employee other_info
    bank_id = fields.Many2one('res.bank')
    account_type_id = fields.Selection([
        ('salary', 'Salary'),
        ('saving', 'Saving'),
        ('current', 'Current')
    ], 'Account type', help='Add employee bank account type')
    bank_record_name = fields.Char('Name as per bank record', tracking=True)
    bank_account_no = fields.Char('Account Number', size=20, help="Max size 20", tracking=True)
    pf_employee = fields.Boolean('Employee covered under of PF', tracking=True)
    uan = fields.Char('UAN', size=12, tracking=True)
    pf_number = fields.Char('PF Number', help="Ex.: AA/AAA/1234567/123/1234567", tracking=True)
    pf_date = fields.Date('PF Join Date', tracking=True)
    family_pf_no = fields.Char('Family PF No', size=50, tracking=True)
    esi_employee = fields.Boolean('Include ESI', tracking=True)
    esi_no = fields.Char('ESI Number', size=50, tracking=True)
    welcome_image = fields.Binary("Welcome Image")

    # Employee identity
    employee_identity_ids = fields.One2many('employee.identity', 'employee_id', 'Employee Identity', required=False)

    # Private Information
    birthday_month = fields.Integer(string='Birthday Month', compute='_compute_birthday_month', store=True)

    # Employee family detail
    family_member_ids = fields.One2many('family.member', 'employee_id', 'Family Members', required=False, tracking=True)

    # Employee Document
    employee_document_ids = fields.One2many('employee.document', 'employee_id', 'Document Detail')
    employee_document_previous_ids = fields.One2many('employee.document', 'employee_id', 'Document Detail',
                                                     domain=[('type', '=', 'past')])
    employee_document_current_ids = fields.One2many('employee.document', 'employee_id', 'Document Detail',
                                                    domain=[('type', '=', 'current')])
    employee_document_education_ids = fields.One2many('employee.document', 'employee_id', 'Document Detail',
                                                      domain=[('type', '=', 'education')])

    # Position history
    position_designation = fields.One2many('designation.history', 'employee_id', 'Designation', required=True,
                                           tracking=True)
    position_location = fields.One2many('location.history', 'employee_id', 'Location', tracking=True)
    position_department = fields.One2many('department.history', 'employee_id', 'Department Name', required=True,
                                          tracking=True)

    position_reporting = fields.One2many('reporting.history', 'employee_id', 'Reporting To', tracking=True)
    position_company = fields.One2many('company.history', 'employee_id', 'Company', tracking=True)

    # Employee resign
    separation_mode = fields.Selection(SEPARATION_MODE, 'Separation Mode')
    left_date = fields.Date('Date', tracking=True)
    remarks = fields.Text('Remarks')
    exitRemark = fields.Text('Exit Remarks')
    demise = fields.Date('Date Of Demise')
    retired_date = fields.Date('Retirement Date', tracking=True)

    # Appraisal
    appraisal_ids = fields.One2many('employee.appraisal', 'employee_id', 'Appraisal Detail', tracking=True)

    # Resignation
    resignation_date = fields.Date('Resignation Submitted On', tracking=True)
    leaving_rason = fields.Selection(
        [('abandoned', 'ABANDONED'), ('contect expire', 'CONTRACT EXPIRE'), ('deported', 'DEPORTED'),
         ('expired', 'EXPIRED'), ('others', 'OTHERS'), ('resigned', 'RESIGNED'), ('retired', 'RETIRED'),
         ('sick', 'SICK'), ('terminated', 'TERMINATED'), ('transferred', 'TRANSFERRED'),
         ('termination', 'TERMINATION ON LEAVE')], 'Reason For Leaving', tracking=True)
    notice_required = fields.Boolean('Notice Required', default=True, tracking=True)
    resigned_notice_period = fields.Integer('Resigned Notice Period', tracking=True)
    short_notice_period = fields.Float('Short Fall in Notice Period', tracking=True)
    tentative_leaving_date = fields.Date('Tentative Leaving Date', tracking=True)
    interview_date = fields.Date('Interview Date', tracking=True)
    note = fields.Text('Note', tracking=True)
    leaving_date = fields.Date('Leaving Date', tracking=True)
    settled_date = fields.Date('Settled Date', tracking=True)
    notice_served = fields.Boolean('Notice Served', tracking=True)
    rehired = fields.Boolean('Fit To Rehired', tracking=True)

    # Employee left organization
    contracted = fields.Boolean('Contracted')
    with_organization = fields.Boolean('Active With Organization', default=True, tracking=True)
    biometric_no = fields.Char("Biometric Code", size=10, tracking=True)
    history = fields.Text('History', tracking=True)
    offer_letter_file = fields.Binary(string="Offer Letter", readonly=True, required=False)
    work_email = fields.Char('Work Email', tracking=True)
    department_id = fields.Many2one('hr.department', 'Department',
                                    domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                    tracking=True)
    parent_id = fields.Many2one('hr.employee', 'Manager', compute="_compute_parent_id", store=True, readonly=False,
                                domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                tracking=True)
    coach_id = fields.Many2one(
        'hr.employee', 'Coach', compute='_compute_coach', store=True, readonly=False,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help='Select the "Employee" who is the coach of this employee.\n'
             'The "Coach" has no specific rights or responsibilities by default.', tracking=True)

    address_id = fields.Many2one('res.partner', 'Work Address', compute="_compute_address_id", store=True,
                                 readonly=False,
                                 domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                 tracking=True)

    work_location_id = fields.Many2one('hr.work.location', 'Work Location', compute="_compute_work_location_id",
                                       store=True, readonly=False,
                                       domain="[('address_id', '=', address_id), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                       tracking=True)

    resource_calendar_id = fields.Many2one('resource.calendar',
                                           domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                           tracking=True)
    tz = fields.Selection(
        string='Timezone', related='resource_id.tz', readonly=False,
        help="This field is used in order to define in which timezone the resources will work.", tracking=True)

    employee_type = fields.Selection([
        ('employee', 'Employee'),
        ('student', 'Student'),
        ('trainee', 'Trainee'),
        ('contractor', 'Contractor'),
        ('freelance', 'Freelancer'),
    ], string='Employee Type', default='employee', required=True, tracking=True,
        help="The employee type. Although the primary purpose may seem to categorize employees, this field has also an impact in the Contract History. Only Employee type is supposed to be under contract and will have a Contract History.")

    job_id = fields.Many2one('hr.job', 'Job Position',
                             domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", tracking=True)

    barcode = fields.Char(string="Badge ID", help="ID used for employee identification.", groups="hr.group_hr_user",
                          copy=False, tracking=True)

    def write(self, vals):
        old_manager = self.parent_id
        res = super(Employee, self).write(vals)
        if 'position_reporting' in vals:
            history = self.env['reporting.history'].search([('employee_id', '=', self.id)], order="effective_from desc",
                                                           limit=1)
            new_manager_obj = self.env['hr.employee'].browse(history.parent_id.id)
            mail_cc = f'{old_manager.work_email}, {new_manager_obj.work_email}'
            template = self.env.ref('aspl_hr_employee.notify_mail_for_manager_change').sudo()
            template_ctx = {'mail_cc': mail_cc,
                            'new_manager_obj': new_manager_obj.name,
                            'effective_from': history.effective_from,
                            }
            template.with_context(template_ctx).send_mail(self.id, force_send=True)

        return res

    def get_attach_id(self, record):
        url = self.env['ir.config_parameter'].get_param('web.base.url')

        if record == 'birth_day_notification':
            attachment_id_face_to_face = self.env.ref('aspl_hr_employee.birthday_image_record').sudo().id
        elif record == '2_year_complete_notification':
            attachment_id_face_to_face = self.env.ref('aspl_hr_employee.2_work_anniversary_image_record').sudo().id
        elif record == '5_year_complete_notification':
            attachment_id_face_to_face = self.env.ref('aspl_hr_employee.5_work_anniversary_image_record').sudo().id
        elif record == '10_year_complete_notification':
            attachment_id_face_to_face = self.env.ref('aspl_hr_employee.10_work_anniversary_image_record').sudo().id

        return url, attachment_id_face_to_face

    def _get_mail_to(self, record):
        mail_to_list_temp = []

        if (
                record != '2_year_complete_notification' and record != '5_year_complete_notification' and record != '10_year_complete_notification'):
            mail_to_list_temp.append(self.parent_id.work_email)
            mail_to_list_temp.append(self.coach_id.work_email)

        attendance_manager_group_users = self.env['res.users'].search(
            [('groups_id', '=', self.env.ref('hr_attendance.group_hr_attendance_manager').sudo().id)])
        hr_employee = self.env['hr.employee'].search(
            [('user_id', 'in', attendance_manager_group_users.ids), ('department_id.name', '=', 'HR & Admin'),
             ('user_id.company_ids', 'in', self.company_id.id)])
        for mail in hr_employee: mail_to_list_temp.append(mail.work_email)

        mail_to_list = list(set(mail_to_list_temp))

        if False in mail_to_list:
            mail_to_list.remove(False)

        if (
                record == '2_year_complete_notification' or record == '5_year_complete_notification' or record == '10_year_complete_notification'):
            mail_to = mail_to_list[0]
        else:
            mail_to = ','.join(mail_to_list)

        return mail_to

    def send_introduction_mail(self):
        url = self.env['ir.config_parameter'].get_param('web.base.url')
        current_date = datetime.today().date()
        employee_ids = self.env['hr.employee'].search(
            ['|', '&', ('join_training_date', '=', current_date), ('employee_no_type', '=', 'trainee'), '&',
             ('join_date', '=', current_date), ('employee_no_type', '!=', 'trainee')])
        for employee in employee_ids:
            emp_ids = self.env['hr.employee'].search(
                [('with_organization', '=', True), ('company_id', '=', employee.company_id.id),
                 ('work_email', '!=', False)])
            bcc_list = list(emp_ids.mapped('work_email'))
            mail_bcc = ','.join(bcc_list)
            context_dict = {
                'employee_name': employee.name,
                'designation': employee.job_title,
                'mail_to': employee.work_email,
                'department': employee.department_id.name,
                'gender': 'he' if employee.gender == 'male' else 'she',
                'mail_cc': mail_bcc if mail_bcc else False,
            }
            if employee.welcome_image:
                image_name = employee.name + 'welcome'
                welcome_image = self.env['ir.attachment'].create(
                    {'name': image_name, 'type': 'binary', 'public': True, 'datas': employee.welcome_image}).sudo().id
                context_dict['welcome_image'] = welcome_image
                context_dict['url'] = url

            template = self.env.ref('aspl_hr_employee.employee_introduction_notifiaction')
            template.with_context(context_dict).send_mail(employee.id, force_send=True)

    # Need to uncomment after script run
    def _get_actual_experience(self):
        for rec in self:
            if rec.resume_line_ids:
                experience_in_day = 0
                for data in rec.resume_line_ids:
                    if data.line_type_id.name == "Experience":
                        if rec.resume_line_ids:
                            for previousEmployment in data:
                                ds = datetime.strftime(previousEmployment.date_start, '%Y:%m:%d')
                                if previousEmployment.date_end:
                                    de = datetime.strftime(previousEmployment.date_end, '%Y:%m:%d')
                                    experience_in_day = int((datetime.strptime(de, '%Y:%m:%d') - datetime.strptime(
                                        ds, '%Y:%m:%d')).days) + experience_in_day

                                else:
                                    experience_in_day = int(
                                        (datetime.now().date() - datetime.strptime(ds,
                                                                                   '%Y:%m:%d').date()).days) + experience_in_day

                year = experience_in_day // 365
                month = (experience_in_day % 365) // 30
                exp = ""
                if year == 1:
                    exp = exp + str(year) + " Year "
                if year > 1:
                    exp = exp + str(year) + " Years "
                if month == 1:
                    exp = exp + str(month) + " Month"
                if month > 1:
                    exp = exp + str(month) + " Months"
                rec.actual_experience = exp
            else:
                rec.actual_experience = 0

    def _get_relative_experience(self):
        for rec in self:
            if rec.resume_line_ids:
                experience_in_day = 0
                for data in rec.resume_line_ids:
                    if data.line_type_id.name == "Experience":
                        if rec.resume_line_ids:
                            for previous_employment in data:

                                if previous_employment.relevant:
                                    ds = datetime.strftime(previous_employment.date_start, '%Y:%m:%d')
                                    if previous_employment.date_end:
                                        de = datetime.strftime(previous_employment.date_end, '%Y:%m:%d')
                                        experience_in_day = int((datetime.strptime(de, '%Y:%m:%d') - datetime.strptime(
                                            ds, '%Y:%m:%d')).days) + experience_in_day

                                    else:
                                        experience_in_day = int(
                                            (datetime.now().date() - datetime.strptime(ds,
                                                                                       '%Y:%m:%d').date()).days) + experience_in_day

                year = experience_in_day // 365
                month = (experience_in_day % 365) // 30
                exp = ""

                if year == 1:
                    exp = exp + str(year) + " Year "
                if year > 1:
                    exp = exp + str(year) + " Years "
                if month == 1:
                    exp = exp + str(month) + " Month"
                if month > 1:
                    exp = exp + str(month) + " Months"
                rec.relative_experience = exp
            else:
                rec.relative_experience = 0

    def _get_experience_graduation(self):
        for rec in self:
            graduation_data = []
            if rec.resume_line_ids:
                for emp_education in rec.resume_line_ids:
                    if emp_education.line_type_id.name == 'Education' and emp_education.date_end:
                        de = datetime.strftime(emp_education.date_end, '%Y:%m:%d')
                        experience_in_day = int((datetime.now().date() - datetime.strptime(de, '%Y:%m:%d').date()).days)
                        graduation_data.append(experience_in_day)
            if len(graduation_data) == 0:
                graduation_data.append(0)

            experience_in_day = min(graduation_data)
            year = experience_in_day // 365
            month = (experience_in_day % 365) // 30
            exp = ""

            if year == 1:
                exp = exp + str(year) + " Year "
            if year > 1:
                exp = exp + str(year) + " Years "
            if month == 1:
                exp = exp + str(month) + " Month"
            if month > 1:
                exp = exp + str(month) + " Months"
            rec.experience_graduation = exp

    def get_week_of_month(self, year, month, day):
        x = np.array(calendar.monthcalendar(year, month))
        week_of_month = np.where(x == day)[0][0] + 1
        return (week_of_month)

    @api.depends('birthday')
    def _compute_birthday_month(self):
        for record in self:
            if record.birthday:
                record.birthday_month = record.birthday.month
            else:
                record.birthday_month = False

    @api.onchange('appraisal_ids')
    def onchange_aprpraisal_ids(self):
        appraisal_date = []
        for rec in self.appraisal_ids:
            appraisal_date.append(rec.appraisal_date)
        if appraisal_date:
            current_appraisal_date = max(appraisal_date)
            new_date = current_appraisal_date + relativedelta(months=12)
            appraisal_date_day = int(new_date.strftime("%d"))
            if appraisal_date_day > 1 and appraisal_date_day > 15:
                date = new_date - relativedelta(days=appraisal_date_day) + relativedelta(days=1) + relativedelta(
                    months=1)
            elif appraisal_date_day > 1 and appraisal_date_day < 15:
                date = new_date - relativedelta(days=appraisal_date_day) + relativedelta(days=1)
            else:
                date = new_date
            self.appraisal_date = date
        else:
            self.appraisal_date = False

    def check_missing_attachment_schedular(self):
        # Preparing a missing attachment dictionary ...
        emp_ids = self.env['hr.employee'].search([('active', '=', True)])
        missing_attachment_emp_dict = {}
        for emp_id in emp_ids:
            if emp_id.with_organization == True:
                # Offer Trainee
                if emp_id.join_training_date:
                    letter_id = emp_id.employee_document_current_ids.filtered(
                        lambda x: x.type_of_document.name == 'Offer Trainee')
                    if not letter_id:
                        if missing_attachment_emp_dict.get(emp_id.name):
                            missing_attachment_emp_dict.get(emp_id.name).append('Offer Trainee')
                        else:
                            missing_attachment_emp_dict.update({emp_id.name: ['Offer Trainee']})

                # Offer Experience
                if not emp_id.join_training_date and emp_id.join_date:
                    letter_id = emp_id.employee_document_current_ids.filtered(
                        lambda x: x.type_of_document.name == 'Offer Experience')
                    if not letter_id:
                        if missing_attachment_emp_dict.get(emp_id.name):
                            missing_attachment_emp_dict.get(emp_id.name).append('Offer Experience')
                        else:
                            missing_attachment_emp_dict.update({emp_id.name: ['Offer Experience']})

                # Appointment
                if emp_id.join_date and emp_id.employee_no_type not in ['consultant_aspire', 'consultant',
                                                                        'consultant_other']:
                    letter_id = emp_id.employee_document_current_ids.filtered(
                        lambda x: x.type_of_document.name == 'Appointment')
                    if not letter_id:
                        if missing_attachment_emp_dict.get(emp_id.name):
                            missing_attachment_emp_dict.get(emp_id.name).append('Appointment')
                        else:
                            missing_attachment_emp_dict.update({emp_id.name: ['Appointment']})

                # Appointment & Increment-Consultant
                if emp_id.join_date and emp_id.employee_no_type in ['consultant_aspire', 'consultant',
                                                                    'consultant_other']:
                    letter_id = emp_id.employee_document_current_ids.filtered(
                        lambda x: x.type_of_document.name == 'Appointment and Increment-Consultant')
                    if not letter_id:
                        if missing_attachment_emp_dict.get(emp_id.name):
                            missing_attachment_emp_dict.get(emp_id.name).append('Appointment and Increment-Consultant')
                        else:
                            missing_attachment_emp_dict.update({emp_id.name: ['Appointment and Increment-Consultant']})

                # Confirmation
                if emp_id.confirm_date:
                    if emp_id.confirm_date <= date.today():
                        letter_id = emp_id.employee_document_current_ids.filtered(
                            lambda x: x.type_of_document.name == 'Confirmation')
                        if not letter_id:
                            if missing_attachment_emp_dict.get(emp_id.name):
                                missing_attachment_emp_dict.get(emp_id.name).append('Confirmation')
                            else:
                                missing_attachment_emp_dict.update({emp_id.name: ['Confirmation']})

                # Appraisal
                appraisal_ids = emp_id.appraisal_ids.filtered(lambda x: x.document == False)
                for appraisal_id in appraisal_ids:
                    if missing_attachment_emp_dict.get(emp_id.name):
                        missing_attachment_emp_dict.get(emp_id.name).append(
                            f'Appraisal - {appraisal_id.appraisal_date.strftime("%d/%m/%Y")}')
                    else:
                        missing_attachment_emp_dict.update(
                            {emp_id.name: [f'Appraisal - {appraisal_id.appraisal_date.strftime("%d/%m/%Y")}']})

            else:
                # Experience & Relieving && Termination
                if emp_id.separation_mode:
                    if emp_id.separation_mode == 'resigned':
                        left_date = emp_id.leaving_date
                    else:
                        left_date = emp_id.left_date
                    if left_date:
                        months_difference = (
                                                    date.today().year - left_date.year) * 12 + date.today().month - left_date.month
                        if months_difference < 4:
                            # Termination
                            if emp_id.separation_mode in ['absconding',
                                                          'terminated'] and emp_id.left_date <= date.today():
                                letter_id = emp_id.employee_document_current_ids.filtered(
                                    lambda x: x.type_of_document.name == 'Termination')
                                if not letter_id:
                                    if missing_attachment_emp_dict.get(emp_id.name):
                                        missing_attachment_emp_dict.get(emp_id.name).append('Termination')
                                    else:
                                        missing_attachment_emp_dict.update({emp_id.name: ['Termination']})
                            # Experience & Relieving
                            elif emp_id.separation_mode == 'resigned' and emp_id.leaving_date <= date.today():
                                letter_id = emp_id.employee_document_current_ids.filtered(
                                    lambda x: x.type_of_document.name == 'Experience and Relieving')
                                if not letter_id:
                                    if missing_attachment_emp_dict.get(emp_id.name):
                                        missing_attachment_emp_dict.get(emp_id.name).append('Experience and Relieving')
                                    else:
                                        missing_attachment_emp_dict.update({emp_id.name: ['Experience and Relieving']})
                            # Experience & Relieving
                            elif emp_id.left_date <= date.today():
                                letter_id = emp_id.employee_document_current_ids.filtered(
                                    lambda x: x.type_of_document.name == 'Experience and Relieving')
                                if not letter_id:
                                    if missing_attachment_emp_dict.get(emp_id.name):
                                        missing_attachment_emp_dict.get(emp_id.name).append('Experience and Relieving')
                                    else:
                                        missing_attachment_emp_dict.update({emp_id.name: ['Experience and Relieving']})

        # mail_to id (HR Resources...)
        mail_to_list = []

        attendance_manager_group_users = self.env['res.users'].search(
            [('groups_id', '=', self.env.ref('hr_attendance.group_hr_attendance_manager').sudo().id)])
        hr_emp_obj = self.env['hr.employee'].search(
            [('user_id', 'in', attendance_manager_group_users.ids), ('department_id.name', '=', 'HR & Admin'),
             ('user_id.company_ids', 'in', [1, 2, 5])])
        for mail in hr_emp_obj: mail_to_list.append(mail.work_email)
        mail_to = ','.join(mail_to_list)

        # Sending Mail ...
        try:
            template_id = self.env.ref('aspl_hr_employee.missing_attachment_mail_template')
            context = {
                'mail_to': mail_to,
                'content': missing_attachment_emp_dict,
            }
            template_id.with_context(context).send_mail(emp_ids.ids[0], force_send=True)

            return True

        except Exception as e:
            # Raise Error
            raise ValidationError(f"Error: {e}")

    def send_termination_letter(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'send.termination.letter',
            'view_type': 'form',
            'view_mode': 'form',
            'name': _('Send Termination letter on mail.'),
            'target': 'new',
            'context': {'employee_id': [self.id]},
        }

    @api.onchange('leaving_date')
    def change_hr_resume_line(self):
        for rec in self:
            last_update = []
            if rec.resume_line_ids:
                for data in rec.resume_line_ids:
                    if data.line_type_id.name == "Experience":
                        last_update.append(data._origin.write_date)
                max_date = max(last_update)
                for data in rec.resume_line_ids:
                    if data.line_type_id.name == "Experience" and not data.date_end:
                        data.write({'date_end': self.leaving_date})
                    elif data.line_type_id.name == "Experience" and data.write_date == max_date:
                        data.write({'date_end': self.leaving_date})

    def cron_celebration_meeting(self):
        employee_id = self.env['hr.employee'].search([])
        for employee in employee_id:
            if employee.id != 21:
                continue

            start = fields.Datetime.now()
            date_b = employee.birthday
            date_m = employee.marriage_date
            date_j = employee.join_date
            restrict_users = 'Support'

            if employee.emp_state == 'left' or employee.department_id.name == restrict_users:
                birthday_event_left = self.env['calendar.event'].search(
                    [('name', 'ilike', 'Birthday'), ('res_id', '=', employee.id)])
                birthday_event_left.unlink()

            elif date_b and employee.with_organization:
                start = start.replace(day=date_b.day, month=date_b.month, hour=0, minute=0, second=0)
                stop = start.replace(day=date_b.day, month=date_b.month, hour=10, minute=59, second=59)

                birthday_count = self.env['calendar.event'].search(
                    [('res_id', '=', employee.id), ('start', '=', start), ('name', 'ilike', 'Birthday')])
                birthday_event = self.env['calendar.event']

                if not birthday_count and not employee.department_id.name == restrict_users:
                    vals = {
                        'name': employee.name + " - Birthday",
                        'res_id': employee.id,
                        'res_model': 'hr.employee',
                        'start': start,
                        'stop': stop,
                    }
                    birthday_event.create(vals)

            if employee.emp_state == 'left' or employee.department_id.name == restrict_users:
                marriage_event_left = self.env['calendar.event'].search(
                    [('name', 'ilike', 'Marriage Anniversery'), ('res_id', '=', employee.id)])
                marriage_event_left.unlink()

            elif date_m and employee.with_organization and date_m.year != start.year:
                start = start.replace(day=date_m.day, month=date_m.month, hour=0, minute=0, second=0)
                stop = start.replace(day=date_m.day, month=date_m.month, hour=10, minute=59, second=59)

                marriage_count = self.env['calendar.event'].search(
                    [('res_id', '=', employee.id), ('start', '=', start), ('name', 'ilike', 'Marriage Anniversery')])
                marriage_event = self.env['calendar.event']

                if not marriage_count and not employee.department_id.name == restrict_users:
                    vals = {
                        'name': employee.name + " - Marriage Anniversery",
                        'res_id': employee.id,
                        'res_model': 'hr.employee',
                        'start': start,
                        'stop': stop,
                    }
                    marriage_event.create(vals)

            if employee.emp_state == 'left' or employee.department_id.name == restrict_users:
                joining_event_left = self.env['calendar.event'].search(
                    [('name', 'ilike', 'Joining Anniversery'), ('res_id', '=', employee.id)])
                joining_event_left.unlink()

            elif date_j and employee.with_organization and date_j.year != start.year:
                start = start.replace(day=date_j.day, month=date_j.month, hour=0, minute=0, second=0)
                stop = start.replace(day=date_j.day, month=date_j.month, hour=10, minute=59, second=59)

                joining_count = self.env['calendar.event'].search(
                    [('res_id', '=', employee.id), ('start', '=', start), ('name', 'ilike', 'Joining Anniversery')])
                joining_event = self.env['calendar.event']

                if not joining_count and not employee.department_id.name == restrict_users:
                    vals = {
                        'name': employee.name + " - Joining Anniversery",
                        'res_id': employee.id,
                        'res_model': 'hr.employee',
                        'start': start,
                        'stop': stop,
                    }
                    joining_event.create(vals)

    def letter(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'employee.letter.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'name': _('Employee Letter'),
            'target': 'new',
            'context': {'employee_id': [self.id]},
        }

    def _state_name(self):
        self.state_name = 'New' if self.emp_state == 'new' else 'Training' \
            if self.emp_state == 'training' else 'Probation' if self.emp_state == 'probation' else 'Notice' \
            if self.emp_state == 'on_notice' else 'Confirmed' if self.emp_state == 'confirmed' else 'Left Organization' \
            if self.emp_state == 'left' else ''

    @api.onchange('training_period')
    def on_change_training_period(self):
        for record in self:
            if record.training_period and record.join_training_date:
                record.training_end_date = record.join_training_date + relativedelta(
                    months=record.training_period)
                record.join_date = record.training_end_date + relativedelta(days=1)

    @api.onchange('probation_period')
    def on_change_probation_period(self):
        for record in self:
            if record.probation_period and record.join_date:
                record.probation_end_date = record.join_date + relativedelta(
                    months=record.probation_period)

    @api.onchange('bond_period')
    def on_change_bond_period(self):
        for record in self:
            if record.bond_period and record.bond_start_date:
                record.bond_end_date = record.bond_start_date + relativedelta(
                    months=record.bond_period)

    @api.onchange('bond_start_date')
    def on_change_bond_start_date(self):
        for record in self:
            if record.bond_period and record.bond_start_date:
                record.bond_end_date = record.bond_start_date + relativedelta(
                    months=record.bond_period)

    @api.onchange('join_date')
    def on_change_join_date(self):
        for record in self:
            if record.probation_period and record.join_date:
                record.probation_end_date = record.join_date + relativedelta(
                    months=record.probation_period)
                record.appraisal_date = record.join_date + relativedelta(months=12)

    @api.onchange('join_training_date')
    def on_change_join_training_date(self):
        for record in self:
            if record.training_period and record.join_training_date:
                record.training_end_date = record.join_training_date + relativedelta(
                    months=record.training_period)
                record.join_date = record.training_end_date + relativedelta(days=1)

    @api.onchange('probation_end_date')
    def on_change_probation_end_date(self):
        for record in self:
            if record.probation_end_date:
                record.confirm_date = record.probation_end_date + relativedelta(days=1)

    @api.onchange('notice_period')
    def onchange_notice_period(self):
        return {'value': {'resigned_notice_period': self.notice_period}}

    @api.onchange('resigned_notice_period')
    def on_change_resigned_notice_period(self):
        for record in self:
            if record.resignation_date:
                dt = datetime.strftime(record.resignation_date, "%Y:%m:%d")
                record.tentative_leaving_date = datetime.strptime(dt, "%Y:%m:%d") + relativedelta(
                    months=record.resigned_notice_period)

    @api.onchange('resignation_date')
    def on_change_resignation_date(self):
        for record in self:
            if record.resignation_date:
                dt = datetime.strftime(record.resignation_date, "%Y:%m:%d")
                record.tentative_leaving_date = datetime.strptime(dt, "%Y:%m:%d") + relativedelta(
                    months=record.resigned_notice_period)

    @api.onchange('leaving_date')
    def on_change_leaving_date(self):
        for rec in self:

            if rec.emp_state == 'on_notice' and rec.separation_mode == 'resigned' and rec.tentative_leaving_date and rec.leaving_date:
                tld = datetime.strftime(rec.tentative_leaving_date, "%Y:%m:%d")
                ld = datetime.strftime(rec.leaving_date, "%Y:%m:%d")
                short_fall_in_day = int((datetime.strptime(tld, "%Y:%m:%d") - datetime.strptime(ld, "%Y:%m:%d")).days)

                tentative_leaving_date = datetime.strptime(tld, "%Y:%m:%d").date()
                leaving_date = datetime.strptime(ld, "%Y:%m:%d").date()
                day_diff = tentative_leaving_date.weekday() - leaving_date.weekday()

                days = ((tentative_leaving_date - leaving_date).days - day_diff) / 7 * 5 + min(day_diff, 5) - (
                        max(tentative_leaving_date.weekday() - 4, 0) % 5)

                if leaving_date.month == tentative_leaving_date.month:
                    if self.get_week_of_month(leaving_date.year, leaving_date.month,
                                              leaving_date.day) == 1 and leaving_date.weekday() <= 5:
                        days = days + 1
                else:
                    if self.get_week_of_month(tentative_leaving_date.year, tentative_leaving_date.month,
                                              tentative_leaving_date.day) > 1:
                        days = days + 1
                    if self.get_week_of_month(tentative_leaving_date.year, tentative_leaving_date.month,
                                              tentative_leaving_date.day) == 1 and tentative_leaving_date.weekday() == 5:
                        days = days + 1
                    if self.get_week_of_month(leaving_date.year, leaving_date.month,
                                              leaving_date.day) == 1 and leaving_date.weekday() <= 5:
                        days = days + 1
                    if (tentative_leaving_date.month - leaving_date.month) > 1:
                        days = days + (tentative_leaving_date.month - leaving_date.month) - 1
                short_fall_in_day = days

                if rec.resignation_date and rec.leaving_date and rec.tentative_leaving_date and rec.user_id:
                    holiday_leave = self.count_holiday_leave(rec.resignation_date, rec.leaving_date)
                    rec.short_notice_period = short_fall_in_day + holiday_leave

    def count_holiday_leave(self, from_date, to_date):
        try:
            domain = [
                ('holiday_from', '<=', to_date),
                ('holiday_from', '>=', from_date),
            ]
            n_holidays = self.env['resource.calendar.leaves'].search_count(domain)
        except ValueError:
            return False
        return n_holidays

    def on_notice(self):
        if self.notice_period > 0:
            self.write({'emp_state': 'on_notice', 'color': 4})
        else:
            raise ValidationError(_('Please Enter "Notice Period"'))
        return True

    def confirmed(self):
        if not self.with_organization:
            hr_obj = self.env['hr.employee'].browse(self.ids)
            confirm_date = datetime.today().date()
            separation_details = 'Separation Mode:' + str(
                hr_obj.separation_mode) + '\n' + 'Resignation Submitted On: ' + str(
                hr_obj.resignation_date) + '\n' + 'Reason For Leaving: ' + str(
                hr_obj.leaving_rason) + '\n' + 'Remarks: ' + '\n' + str(hr_obj.remarks) + '\n' + str(
                hr_obj.left_date) + '\n' + 'Left Date: ' + str(hr_obj.left_date)
            hr_obj.write({
                'emp_state': 'confirmed',
                'color': 8,
                'history': separation_details,
                'with_organization': True,
                'confirm_date': confirm_date
            })
            user_obj = self.env['res.users'].search([('id', '=', hr_obj.user_id.id)])
            user_obj.write({
                'active': True
            })
            try:
                self.user_id.write({
                    'active': True
                })

            except Exception as e:
                _logger.error('Error while adding Leaves')
                _logger.error(str(e))
                traceback.format_exc()

        else:
            confirm_date = self.confirm_date
            if confirm_date:
                dt = datetime.strftime(self.confirm_date, '%Y:%m:%d')
                if datetime.strptime(dt, '%Y:%m:%d').date() <= datetime.today().date():
                    self.write({'emp_state': 'confirmed', 'color': 8})
                    self.with_organization = True
                else:
                    raise ValidationError(_('Please Enter correct "Confirm Date"'))
            else:
                raise ValidationError(_('Please Enter "Confirm Date"'))

        return True

    def training(self):
        if not self.with_organization:
            hr_obj = self.env['hr.employee'].browse(self.ids)
            separation_details = 'Separation Mode: ' + str(
                hr_obj.separation_mode) + '\n' + 'Resignation Submitted On: ' + str(
                hr_obj.resignation_date) + '\n' + 'Reason For Leaving: ' + str(
                hr_obj.leaving_rason) + '\n' + 'Remarks: ' + '\n' + str(hr_obj.remarks) + '\n' + str(
                hr_obj.left_date) + '\n' + 'Left Date: ' + str(hr_obj.left_date)
            hr_obj.write({
                'emp_state': 'training',
                'history': separation_details,
                'with_organization': True
            })
            user_obj = self.env['res.users'].search([('id', '=', hr_obj.user_id.id)])
            user_obj.write({
                'active': True
            })
        else:
            if self.join_training_date:
                dt = datetime.strftime(self.join_training_date, '%Y:%m:%d')
            else:
                raise ValidationError(_('Please Enter correct "Training start date"'))

            if self.training_period > 0:
                if datetime.strptime(dt, "%Y:%m:%d").date() <= datetime.today().date():
                    self.write({'emp_state': 'training', 'color': 9})
                else:
                    raise ValidationError(_('Please Enter correct "Training start date"'))
            else:
                raise ValidationError(_('Please Enter "Training Period"!!'))
        return True

    def probation(self):
        if not self.with_organization:
            hr_obj = self.env['hr.employee'].browse(self.ids)
            join_date = datetime.today().date()
            separation_details = 'Separation Mode: ' + str(
                hr_obj.separation_mode) + '\n' + 'Resignation Submitted On: ' + str(
                hr_obj.resignation_date) + '\n' + 'Reason For Leaving: ' + str(
                hr_obj.leaving_rason) + '\n' + 'Remarks: ' + '\n' + str(hr_obj.remarks) + '\n' + str(
                hr_obj.left_date) + '\n' + 'Left Date: ' + str(hr_obj.left_date)
            self.write({
                'emp_state': 'probation',
                'color': 6,
                'history': separation_details,
                'with_organization': True,
                'join_date': join_date
            })
            self.on_change_join_date()
            self.on_change_probation_end_date()
            user_obj = self.env['res.users'].search([('id', '=', hr_obj.user_id.id)])
            user_obj.write({
                'active': True
            })

        else:
            if self.join_date:
                jdt = datetime.strftime(self.join_date, '%Y:%m:%d')
                if datetime.strptime(jdt, '%Y:%m:%d').date() <= datetime.today().date():
                    if self.probation_period > 0:
                        if self.emp_state == 'new':
                            self.write({'emp_state': 'probation', 'color': 6})
                            self.with_organization = True
                            current_year = datetime.now().year
                            if current_year != 2015:
                                try:

                                    if self.employee_no_type != 'consultant':
                                        self.write({'employee_no_type': 'permanent_employee'})

                                except Exception as e:
                                    _logger.error('Something is wrong')
                                    _logger.error(str(e))
                                    traceback.format_exc()

                        elif self.emp_state == 'training':
                            if self.join_training_date:
                                dt = datetime.strftime(self.join_training_date, '%Y:%m:%d')
                                if datetime.strptime(dt, '%Y:%m:%d').date() <= datetime.today().date():
                                    self.write({'emp_state': 'probation', 'color': 6})
                                    self.with_organization = True
                                    current_year = datetime.now().year
                                    if current_year != 2015:
                                        try:
                                            if str(self.employee_no_type).lower() == "trainee":

                                                self.write({'trainee_no': self.employee_no})
                                                if self.employee_no_type != 'consultant':
                                                    self.write({'employee_no_type': 'permanent_employee'})
                                        except Exception as e:
                                            _logger.error('Something is wrong')
                                            _logger.error(str(e))
                                            traceback.format_exc()
                            else:
                                raise ValidationError(_('Please Enter correct "Training start date"'))
                    else:
                        raise ValidationError(_('Please Enter "Probation Period"!!'))
                else:
                    raise ValidationError(_('Please Enter correct "Join Date"!!'))
            else:
                raise ValidationError(_('Please Enter "Join Date"!!'))

        return True

    # Employee with organization change false with change in separation mode
    def on_left_org(self):
        employee_obj = self.env['hr.employee'].search([('id', '=', self.ids)])
        employee_obj.write({
            'emp_state': 'left',
            'with_organization': False,
        })
        user_obj = self.env['res.users'].search([('id', '=', employee_obj.user_id.id)])
        user_obj.write({
            'active': False
        })

    @api.onchange('isPresentAddSameAsPermanent')
    def on_change_is_Present_Add_Same_As_Permanent(self):
        for record in self:
            if record.isPresentAddSameAsPermanent:
                record.pre_street = record.per_street
                record.pre_landmark = record.per_landmark
                record.pre_city = record.per_city
                record.pre_pcode = record.per_pcode
                record.pre_state_id = record.per_state_id
                record.pre_county_id = record.per_county_id
                record.pre_phone1 = record.per_phone1
                record.pre_phone2 = record.per_phone2
            else:
                record.pre_street = None
                record.pre_landmark = None
                record.pre_city = None
                record.pre_pcode = None
                record.pre_state_id = None
                record.pre_county_id = None
                record.pre_phone1 = None
                record.pre_phone2 = None

    @api.onchange('per_street')
    def on_change_pre_street(self):
        for record in self:
            if record.isPresentAddSameAsPermanent:
                record.pre_street = record.per_street

    @api.onchange('per_landmark')
    def on_change_per_landmark(self):
        for record in self:
            if record.isPresentAddSameAsPermanent:
                record.pre_landmark = record.per_landmark

    @api.onchange('per_city')
    def on_change_per_city(self):
        for record in self:
            if record.isPresentAddSameAsPermanent:
                record.pre_city = record.per_city

    @api.onchange('per_pcode')
    def on_change_per_pcode(self):
        for record in self:
            if record.isPresentAddSameAsPermanent:
                record.pre_pcode = record.per_pcode

    @api.onchange('per_state_id')
    def on_change_per_state_id(self):
        for record in self:
            if record.isPresentAddSameAsPermanent:
                record.pre_state_id = record.per_state_id

    @api.onchange('per_county_id')
    def on_change_per_county_id(self):
        for record in self:
            if record.isPresentAddSameAsPermanent:
                record.pre_county_id = record.per_county_id

    @api.onchange('per_phone1')
    def on_change_per_phone1(self):
        for record in self:
            if record.isPresentAddSameAsPermanent:
                record.pre_phone1 = record.per_phone1

    @api.onchange('per_phone2')
    def on_change_per_phone2(self):
        for record in self:
            if record.isPresentAddSameAsPermanent:
                record.pre_phone2 = record.per_phone2

    @api.constrains('work_email', 'per_phone1', 'personal_email')
    def _check_constraints(self):
        if self.per_phone1:
            flag = Validation.check_phone(self.per_phone1)
            if not flag:
                raise ValidationError(Constant.INVALID_MOBILE_NO)
        if self.work_email:
            flag = Validation.check_email(self.work_email)
            if not flag:
                raise ValidationError(Constant.INVALID_WORK_EMAIL)
        if self.personal_email:
            flag = Validation.check_email(self.personal_email)
            if not flag:
                raise ValidationError(Constant.INVALID_PERSONAL_EMAIL)
        return True

    def current_employee_form(self):
        exist = self.sudo().search([["user_id", "=", self.env.uid]], limit=1)

        view_id = self.env['ir.ui.view'].search([('name', '=', 'hr.own.employee.form')])

        return {
            "type": "ir.actions.act_window",
            "res_model": 'hr.employee',
            "view_mode": "form",
            "name": _('Information'),
            "view_id": view_id.id,
            "res_id": exist.id if exist.id else False
        }


class StDataSet(DataSet):
    # Odoo Core Web Module method override for manage own access in employee

    def call_kw(self, model, method, args, kwargs,path=None):
        if model == 'hr.employee' and method in ('read','web_read'):
            group_hr_manager = request.env.user.has_group('hr.group_hr_manager')
            employees = request.env['hr.employee'].browse(args[0])
            if group_hr_manager:
                pass
            else:
                if len(employees) == 1:
                    if employees is not None:
                        if employees.user_id.id != request.uid and employees.parent_id.user_id.id != request.uid:
                            raise UserError(
                                _("You are not allowed to access this employee. Please contact to your administrator."))

        check_method_name(method)
        return call_kw(request.env[model], method, args, kwargs)
