# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import os
import subprocess
from odoo.exceptions import ValidationError

from odoo import models, fields


class SendTerminationLetter(models.TransientModel):
    _name = 'send.termination.letter'
    _description = "Send Termination Letter"

    description = fields.Char(string="Description",
                              default="Are you sure you want to send the termination letter email? Please confirm your action.")

    def send_email_employee(self):
        employee_obj = self.env['hr.employee'].browse(self.env.context.get('employee_id'))

        # Calling Generate Letter Function From 'employee.letter.wizard' ...
        ctx = dict(self.env.context)
        ctx.update({'termination_letter': True})
        attachment_id = self.env['employee.letter.wizard'].with_context(ctx).generate_employee_letter()

        # Send Termination Letter on Employee Personal Mail id ...
        try:
            template_id = self.env.ref('aspl_hr_employee.termination_letter_mail_template')
            context = {
                'mail_to': employee_obj.personal_email,
            }

            # Create a temporary path for the Word document
            word_document_path = '/tmp/' + attachment_id.name
            with open(word_document_path, 'wb') as word_file:
                word_file.write(base64.b64decode((attachment_id.datas)))

            # Specify the path for the output PDF file
            pdf_output_path = '/tmp/' + attachment_id.name.replace('.docx', '.pdf')

            # Convert Word document to PDF using LibreOffice
            command = ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', '/tmp', word_document_path]
            subprocess.run(command)

            # Read the resulting PDF data
            pdf_attachment_data = open(pdf_output_path, 'rb').read()

            # Create a new attachment record for the PDF
            vals = {
                'name': attachment_id.name.replace('.docx', '.pdf'),
                'datas': base64.b64encode(pdf_attachment_data),
                'store_fname': attachment_id.name.replace('.docx', '.pdf'),
                'res_model': 'hr.employee',
                'res_id': self.id,
            }
            pdf_attachment = self.env['ir.attachment'].create(vals)

            template_id.attachment_ids = [(6, 0, pdf_attachment.ids)]
            template_id.with_context(context).send_mail(employee_obj.id, force_send=True)

            # Remove Pdf Attachment & OS Directory tmp Files
            os.remove(word_document_path)
            os.remove(pdf_output_path)
            pdf_attachment.unlink()

            return True

        except Exception as e:
            # Raise Error
            raise ValidationError(f"Error: {e}")
