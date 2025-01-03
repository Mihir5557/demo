# -*- coding: utf-8 -*-

{
    'name': "Aspire Employee",
    'version': '18.0.0.0.1',
    'description': "",
    'author': 'Aspire Softserv Private Limited',
    'website': "https://aspiresoftware.in",
    'summary': '',
    'category': 'Employee',
    'depends': ['hr',
                'hr_recruitment',
                'contacts',
                'hr_holidays',
                'hr_skills',
                'website',
                'base',
                'hr_holidays_attendance'
                ],
    "external_dependencies": {
        'python': [
            'docx',

        ]
    },
    'data': [
        'security/ir.model.access.csv',
        'data/notifier_mail_template.xml',
        'data/hr_employee_stage_data.xml',
        'data/employee_document_type_data.xml',
        'data/employee_document_category_data.xml',
        'data/notifier_schedular.xml',
        'data/missing_attachment_schedular.xml',
        'sequence/auto_id.xml',
        'views/hr_employee_view.xml',
        'views/hr_employee_stage_view.xml',
        'views/hr_letters_view.xml',
        'views/identity_view.xml',
        'views/hr_own_employee_view.xml',
        'views/hr_all_employee_view.xml',
        'views/hr_resume_line_view.xml',
        'views/notifier_view.xml',
        'views/birth_day_view.xml',
        'views/employee_configuration.xml',
        'views/employee_document_type_view.xml',
        'views/employee_document_category_view.xml',
        'wizards/employee_letter.xml',
        'wizards/send_termination_letter_view.xml',
        'wizards/regeneration_letter_permission_view.xml',
        'reports/accept_reject_template_view.xml',
        'reports/termination_letter_mail.xml',
        'reports/missing_attachment_mail.xml',
        'reports/regeneration_letter_permission_mail.xml',
        'reports/accept_reject_return_mail.xml',
    ],
    'installable': True,
    'sequence': 12,
    'license': 'LGPL-3',
    'auto_install': False
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
