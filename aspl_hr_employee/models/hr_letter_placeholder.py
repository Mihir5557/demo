# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import date

from odoo import models, fields, api

ordinal_suffix_days = {1: 'st', 2: 'nd', 3: 'rd'}
today = date.today()

STATIC_FIELDS = [('emp_address', 'Employee Address'), ('company_address', 'Company Address'),
                 ('ms/mr/miss', 'Ms./Mr./Miss'),
                 ('her/him', 'her/him'), ('her/his', 'her/his'), ('today', 'Today'),
                 ('sal_rev_dt', 'Salary Revision Date(Date / Month)'),
                 ('con_eff_dt', "Consultant Effective Date's Timeline(Join_date to After 1 Year Date)"),
                 ('con_app_dt',
                  "Consultant Appraisal Date's Timeline(appraisal_date and terminating on terminating_date)"),
                 ('app_exis_year', "Appraisal Existing Year(from_year to year)"),
                 ('app_new_year', "Appraisal New Year(from_year to year)"),
                 ('salary_annual_ctc_word', "Annual CTC(Rs. 00/- (Rupees -- Only))"),
                 ('salary_monthly_ctc_word', "Monthly CTC(Rs. 00/- (Rupees -- Only))"),
                 ('salary_monthly_ctc', "Monthly CTC(For Table Value)"),
                 ('salary_Yearly_ctc', "Annual CTC(For Table Value)"),
                 ('salary_monthly_gratuity', "Monthly Gratuity(For Table Value)"),
                 ('salary_Yearly_gratuity', "Annual Gratuity(For Table Value)"),
                 ('salary_monthly_pf_er', "Monthly Employer PF(For Table Value)"),
                 ('salary_Yearly_pf_er', "Annual Employer PF(For Table Value)"),
                 ('salary_monthly_esic_er', "Monthly Employer ESIC(For Table Value)"),
                 ('salary_Yearly_esic_er', "Annual Employer ESIC(For Table Value)"),
                 ('salary_monthly_basic', "Monthly Basic(For Table Value)"),
                 ('salary_Yearly_basic', "Annual Basic(For Table Value)"),
                 ('salary_monthly_hra', "Monthly HRA(For Table Value)"),
                 ('salary_Yearly_hra', "Annual HRA(For Table Value)"),
                 ('salary_monthly_allowance', "Monthly Other Allowance(For Table Value)"),
                 ('salary_Yearly_allowance', "Annual Other allowance(For Table Value)"),
                 ('salary_monthly_gross', "Monthly Total Gross(For Table Value)"),
                 ('salary_Yearly_gross', "Annual Total Gross(For Table Value)"),
                 ('salary_monthly_pt', "Monthly Pro Tax(For Table Value)"),
                 ('salary_Yearly_pt', "Annual Pro Tax(For Table Value)"),
                 ('salary_monthly_pf_ee', "Monthly Employee PF(For Table Value)"),
                 ('salary_Yearly_pf_ee', "Annual Employee PF(For Table Value)"),
                 ('salary_monthly_esic_ee', "Monthly Employee ESIC(For Table Value)"),
                 ('salary_Yearly_esic_ee', "Annual Employee ESIC(For Table Value)"),
                 ('salary_monthly_net', "Monthly Total Net(For Table Value)"),
                 ('salary_Yearly_net', "Annual Total Net(For Table Value)"),
                 ]


class HrLetterPlaceholders(models.Model):
    _name = "hr.letter.placeholders"
    _description = "Hr Letter Placeholders"
    _order = "write_date desc"

    hr_letters_id = fields.Many2one('hr.letters', string='Hr Letters')

    # expression builder
    # Cofigration Of Field's
    fields_direction = fields.Selection([('dynamic', "Make Dynamic Field's"), ('static', "Make Static Field's")],
                                        string="Field's Direction",
                                        default='dynamic')

    # static Field's
    static_fields = fields.Selection(STATIC_FIELDS, string="Static Field's")

    # Dynamic Field's
    model_object = fields.Many2one('ir.model', string="Menu's")
    field_object = fields.Many2one('ir.model.fields', string='Field')
    field_object_type = fields.Selection(related='field_object.ttype', string='Field Object Type')
    sub_model_object = fields.Many2one('ir.model', string="Sub Menu's")
    sub_field_object = fields.Many2one('ir.model.fields', string='Sub Field')
    sub_field_object_type = fields.Selection(related='sub_field_object.ttype', string='Sub Field Object Type')
    date_format = fields.Selection([('0', '%d %B, %Y'), ('1', '%d / %m / %Y'), ('2', '%d - %m - %Y')],
                                   string="Date Format")
    sample_date_format = fields.Char(string='Sample Date Format')
    num2word = fields.Boolean(string='Convert Num2Word ?')

    # Expression
    placeholder_expression = fields.Char(string='Placeholder Expression')

    @api.model
    def _build_expression(self, sub_field_object_type, extra_feature):
        if sub_field_object_type:
            if extra_feature:
                expression = "{{ " + str(
                    self.field_object.model_id.model) + " - " + self.field_object.name + " - " + self.sub_field_object.name + " - " + sub_field_object_type + " - " + extra_feature + " }}"
            else:
                expression = "{{ " + str(
                    self.field_object.model_id.model) + " - " + self.field_object.name + " - " + self.sub_field_object.name + " - " + sub_field_object_type + " }}"
        else:
            if extra_feature:
                expression = "{{ " + str(
                    self.field_object.model_id.model) + " - " + self.field_object.name + " - " + extra_feature + " }}"
            else:
                expression = "{{ " + str(self.field_object.model_id.model) + " - " + self.field_object.name + " }}"

        return expression

    @api.onchange('fields_direction', 'static_fields', 'model_object', 'field_object', 'sub_field_object',
                  'date_format', 'num2word')
    def _onchange_dynamic_placeholder(self):
        if self.fields_direction == 'dynamic':
            if self.static_fields:
                self.static_fields = False
                self.placeholder_expression = False

            if self.sub_field_object:
                if self.field_object:
                    if self.model_object:
                        if self.sub_field_object_type == "many2many":
                            sub_field_object_type = "m2m"
                        elif self.sub_field_object_type == "many2one":
                            sub_field_object_type = "m2o"
                        else:
                            sub_field_object_type = "o2m"

                        if self.sub_field_object_type in ['date', 'datetime']:
                            if self.date_format:
                                if self.date_format == '0':
                                    day = today.day
                                    day_suffix = ordinal_suffix_days.get(day,
                                                                         'th') if 10 <= day % 100 <= 20 else ordinal_suffix_days.get(
                                        day % 10, 'th')
                                    self.sample_date_format = today.strftime(f'%d{day_suffix} %B, %Y')
                                    self.placeholder_expression = self._build_expression(sub_field_object_type,
                                                                                         "%dth %B, %Y")
                                elif self.date_format == '1':
                                    self.sample_date_format = today.strftime("%d/%m/%Y")
                                    self.placeholder_expression = self._build_expression(sub_field_object_type,
                                                                                         "%d/%m/%Y")
                                else:
                                    self.sample_date_format = today.strftime("%d-%m-%Y")
                                    self.placeholder_expression = self._build_expression(sub_field_object_type,
                                                                                         "%d-%m-%Y")
                            else:
                                self.placeholder_expression = self._build_expression(sub_field_object_type, False)
                                self.sample_date_format = False
                        elif self.sub_field_object_type in ['float', 'integer', 'monetary']:
                            if self.num2word:
                                self.placeholder_expression = self._build_expression(sub_field_object_type, "n2w")
                            else:
                                self.placeholder_expression = self._build_expression(sub_field_object_type, False)
                        else:
                            self.placeholder_expression = self._build_expression(sub_field_object_type, False)
                    else:
                        self.sub_model_object = False
                        self.sub_field_object = False
                else:
                    self.sub_model_object = False
                    self.sub_field_object = False
            elif self.field_object:
                if self.model_object:
                    if self.sub_model_object:
                        self.placeholder_expression = False
                    else:
                        if self.field_object_type in ['many2many', 'many2one', 'one2many']:
                            self.sub_model_object = self.env['ir.model']._get(self.field_object.relation)
                            self.placeholder_expression = False
                        elif self.field_object_type in ['date', 'datetime']:
                            if self.date_format:
                                if self.date_format == '0':
                                    day = today.day
                                    day_suffix = ordinal_suffix_days.get(day,
                                                                         'th') if 10 <= day % 100 <= 20 else ordinal_suffix_days.get(
                                        day % 10, 'th')
                                    self.sample_date_format = today.strftime(f'%d{day_suffix} %B, %Y')
                                    self.placeholder_expression = self._build_expression(False, "%dth %B, %Y")
                                elif self.date_format == '1':
                                    self.sample_date_format = today.strftime("%d/%m/%Y")
                                    self.placeholder_expression = self._build_expression(False, "%d/%m/%Y")
                                else:
                                    self.sample_date_format = today.strftime("%d-%m-%Y")
                                    self.placeholder_expression = self._build_expression(False, "%d-%m-%Y")
                            else:
                                self.placeholder_expression = self._build_expression(False, False)
                                self.sample_date_format = False
                        elif self.field_object_type in ['float', 'integer', 'monetary']:
                            if self.num2word:
                                self.placeholder_expression = self._build_expression(False, "n2w")
                            else:
                                self.placeholder_expression = self._build_expression(False, False)
                        else:
                            self.placeholder_expression = self._build_expression(False, False)
                else:
                    self.field_object = False
            else:
                self.placeholder_expression = False
        else:
            if self.model_object or self.field_object or self.sub_field_object:
                self.model_object = False
                self.field_object = False
                self.sub_field_object = False
                self.placeholder_expression = False

            if self.static_fields:
                if self.static_fields in ['today']:
                    if self.date_format:
                        if self.date_format == '0':
                            day = today.day
                            day_suffix = ordinal_suffix_days.get(day,
                                                                 'th') if 10 <= day % 100 <= 20 else ordinal_suffix_days.get(
                                day % 10, 'th')
                            self.sample_date_format = today.strftime(f'%d{day_suffix} %B, %Y')
                            self.placeholder_expression = "{{ " + self.static_fields + ".%dth %B, %Y" + " }}"
                        elif self.date_format == '1':
                            self.sample_date_format = today.strftime("%d/%m/%Y")
                            self.placeholder_expression = "{{ " + self.static_fields + ".%d/%m/%Y" + " }}"
                        else:
                            self.sample_date_format = today.strftime("%d-%m-%Y")
                            self.placeholder_expression = "{{ " + self.static_fields + ".%d-%m-%Y" + " }}"
                    else:
                        self.sample_date_format = False
                        self.placeholder_expression = False
                else:
                    self.placeholder_expression = "{{ " + self.static_fields + " }}"
            else:
                self.placeholder_expression = False
