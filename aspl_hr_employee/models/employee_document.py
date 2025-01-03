# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import logging
from odoo.exceptions import ValidationError

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


# Employee family information
class EmployeeDocument(models.Model):
    _name = "employee.document"
    _description = "Employee Document"

    employee_id = fields.Many2one('hr.employee', 'Employee')
    document_name = fields.Char('Attachment Name', required=True)
    report_type = fields.Selection([
        ('pdf', 'PDF'),
        ('word', 'Word'),
        ('other', 'Other'),
    ], 'Report Type', required=True)
    document_description = fields.Text('Description')
    document = fields.Binary('Document', required=True)
    attached_date = fields.Date('Attached Date', default=fields.Date.context_today)
    type = fields.Selection(string='Type',
                            selection=[('past', 'Previous employment'),
                                       ('current', 'Current employment'),
                                       ('education', 'Education'),
                                       ],
                            required=True)
    type_of_document = fields.Many2one('employee.document.type', string='Type Of Document', required=True)
    status = fields.Selection(string='Status', selection=[('lock', 'Lock'),
                                                          ('unlock', 'Unlock'),
                                                          ], default='lock')
    accept_token = fields.Char('Accept Token')
    reject_token = fields.Char('Reject Token')

    @api.constrains('report_type', 'document')
    def _check_document_type(self):
        for record in self:
            if record.report_type == 'pdf':
                file_name = base64.b64decode(record.document)
                if not file_name.startswith(b'%PDF'):
                    raise ValidationError('For PDF reports, please upload a PDF file.')
            if record.report_type == 'word':
                file_name = base64.b64decode(record.document)
                if not file_name.startswith(b'PK'):
                    raise ValidationError('For Word reports, please upload a Word file.')

    def unlink(self):
        for rec in self:
            employee_obj = rec.employee_id
            type_of_document = rec.type_of_document.name
            res = super(EmployeeDocument, self).unlink()

            # Add Log Note
            employee_obj.message_post(body="%s Document deleted." % type_of_document)

        return res

    def download_document(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/binary/download_document?model=employee.document&doc_field=document&rec_id=%s&filename=%s' % (
                self.id, self.document_name),
            'target': 'self',
        }
