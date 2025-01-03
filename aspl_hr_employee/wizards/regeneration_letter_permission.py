# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.exceptions import ValidationError

from odoo import models, fields


class RegenerationLetterPermission(models.TransientModel):
    _name = 'regeneration.letter.permission'
    _description = "Regeneration Letter Permission"

    description = fields.Char(string="Description",
                              default='The Letter you selected has been already issued and it is locked for modification click "Request Unlock" to get it unlocked by system administrator.')

    def send_email_administrator(self):
        employee_obj = self.env['hr.employee'].browse(self.env.context.get('employee_id'))
        letter_obj = self.env[self.env.context.get('letter_model')].browse(int(self.env.context.get('letter_id')))

        # mail_to id (Access Settings Groups ...)
        mail_to_list = []

        administrator_setting_group_users = self.env['res.users'].search(
            [('groups_id', '=', self.env.ref('base.group_system').sudo().id), ('company_id', 'in', [1, 2, 5])])
        for user_obj in administrator_setting_group_users: mail_to_list.append(user_obj.email)
        mail_to = ','.join(mail_to_list)

        args_values = f"employee_id={self.env.context.get('employee_id')}&letter_model={self.env.context.get('letter_model')}&letter_id={self.env.context.get('letter_id')}&sender_mail={self.env.user.email}&receiver_mail={mail_to}&letter_name={letter_obj.document_name}"

        # Send Regeneration Letter Permission on Administrator Mail id ...
        try:
            template_id = self.env.ref('aspl_hr_employee.regeneration_letter_permission_mail_template')
            context = {
                'acceptRegenerationLetterPermissionURL': f"/regeneration/letter/permission/accept?{args_values}",
                'rejectRegenerationLetterPermissionURL': f"/regeneration/letter/permission/reject?{args_values}",
                'mail_to': mail_to,
                'letter_name': letter_obj.document_name,
            }
            template_id.with_context(context).send_mail(employee_obj.id, force_send=True)

            return True

        except Exception as e:
            # Raise Error
            raise ValidationError(f"Error: {e}")
