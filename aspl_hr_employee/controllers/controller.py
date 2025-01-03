# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import werkzeug.urls
from odoo.exceptions import ValidationError
from odoo.http import request, content_disposition

from odoo import http


class RegenerationLetterPermissionController(http.Controller):

    @http.route(['/regeneration/letter/permission/accept', '/regeneration/letter/permission/reject'], type="http",
                auth="user", website=True)
    def index(self, **kwargs):
        route = request.httprequest.path
        letter_obj = request.env[kwargs.get('letter_model')].browse(int(kwargs.get('letter_id')))

        if letter_obj:
            # Check Route Path
            if route == "/regeneration/letter/permission/accept":
                letter_obj.reject_token = False

                # Check For the Double Click Button or not ...
                if letter_obj.accept_token:

                    return request.render('aspl_hr_employee.admin_double_click_template', {})
                else:
                    # Change Report Status Lock to Unlock
                    letter_obj.status = 'unlock'

                    # Set Accept Token Value
                    letter_obj.accept_token = werkzeug.urls.url_encode({'uid': letter_obj.id})

                    # Send Accept Return Mail
                    try:
                        template_id = request.env.ref('aspl_hr_employee.accept_return_mail_template')
                        context = {
                            'sender_mail': kwargs.get('sender_mail'),
                            'receiver_mail': kwargs.get('receiver_mail').split(',')[0].strip(),
                            'letter_name': kwargs.get('letter_name'),
                        }
                        template_id.with_context(context).sudo().send_mail(int(kwargs.get('employee_id')),
                                                                           force_send=True)

                        return request.render('aspl_hr_employee.accept_admin_template', {})

                    except Exception as e:
                        # Raise Error
                        raise ValidationError(f"Error: {e}")
            else:
                letter_obj.accept_token = False

                # Check For the Double Click Button or not ...
                if letter_obj.reject_token:

                    return request.render('aspl_hr_employee.admin_double_click_template', {})
                else:
                    # Change Report Status Unlock to Lock
                    letter_obj.status = 'lock'

                    # Set Reject Token Value
                    letter_obj.reject_token = werkzeug.urls.url_encode({'uid': letter_obj.id})

                    # Send Reject Return Mail
                    try:
                        template_id = request.env.ref('aspl_hr_employee.reject_return_mail_template')
                        context = {
                            'sender_mail': kwargs.get('sender_mail'),
                            'receiver_mail': kwargs.get('receiver_mail').split(',')[0].strip(),
                            'letter_name': kwargs.get('letter_name'),
                        }
                        template_id.with_context(context).sudo().send_mail(int(kwargs.get('employee_id')),
                                                                           force_send=True)

                        return request.render('aspl_hr_employee.reject_admin_template', {})

                    except Exception as e:
                        # Raise Error
                        raise ValidationError(f"Error: {e}")
        else:
            return request.render('aspl_hr_employee.letter_not_found_template', {})


class Binary(http.Controller):

    @http.route('/web/binary/download_document', type='http', auth="public")
    def download_document(self, model, **kw):
        rec_id = int(kw.get('rec_id'))
        doc_field = kw.get('doc_field')
        identity = request.env[model].browse(rec_id).read([doc_field])
        filecontent = base64.b64decode(identity[0].get(doc_field))
        filename = kw.get('filename')
        return request.make_response(filecontent,
                                     [('Content-Type', 'application/pdf'),
                                      ('Content-Disposition', content_disposition(filename))])
