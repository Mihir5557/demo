# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import date

from odoo import models, fields, api, _


class HrLetters(models.Model):
    _name = 'hr.letters'
    _description = 'HR Letters'
    _rec_name = 'name'

    name = fields.Char('Name')
    attachment = fields.Binary(string="Attachment")
    allowed_in_stages = fields.Many2many('hr.employee.stage', string="Allowed in stages")
    document_type_id = fields.Many2one('employee.document.type', string='Letter Type')
    hr_letter_placeholders_line_ids = fields.One2many('hr.letter.placeholders', 'hr_letters_id', string='Placeholders')
    letter_version_control_line_ids = fields.One2many('hr.letter.version.control', 'letters_version_control_id',
                                                      string='Version Control')

    @api.onchange('name')
    def _onchange_document_name(self):
        for rec in self:
            if rec.name:
                if '.docx' in rec.name:
                    rec.name = rec.name.replace('.docx', '')

    @api.model
    def create(self, vals):
        res = super(HrLetters, self).create(vals)

        if vals.get('attachment') and vals.get('name'):
            values = {
                'letters_version_control_id': res.id,
                'name': vals.get('name'),
                'attachment_v_c': vals.get('attachment'),
            }
            self.env['hr.letter.version.control'].create(values)

            return res

    def write(self, vals):
        res = super(HrLetters, self).write(vals)

        if vals.get('attachment'):
            values = {
                'letters_version_control_id': self.id,
                'name': vals.get('name'),
                'attachment_v_c': vals.get('attachment'),
            }
            self.env['hr.letter.version.control'].create(values)
        return res


class HrLetterVersionControl(models.Model):
    _name = "hr.letter.version.control"
    _description = "Hr Letter Version Control"
    _order = "write_date desc"

    letters_version_control_id = fields.Many2one('hr.letters', string='Hr Letters')
    name = fields.Char('Name')
    attachment_v_c = fields.Binary(string="Attachment")
