# -*- coding: utf-8 -*-
###############################################################################
#
# Aspire Softserv Pvt. Ltd.
# Copyright (C) Aspire Softserv Pvt. Ltd.(<https://aspiresoftserv.com>).
#
###############################################################################
{
    'name': 'Appraisal',
    'category': 'Human Resources/Appraisal',
    'summary': 'Appraisal Management',
    'version': '18.0.0.1.0',
    "license": "AGPL-3",
    'description': 'Module to manage employee appraisals',
    'author': 'Aspire Softserv Pvt. Ltd',
    'website': 'https://aspiresoftserv.com',
    'depends': ['base',
                'hr',
                'mail',
                'calendar',
                'survey',
                'aspl_hr_employee'],
    'data': [
        'security/ir.model.access.csv',
        'security/hr_appraisal_security.xml',
        'data/data.xml',
        'data/mail_template_data.xml',
        'data/hr_appraisal_survey_data.xml',
        'views/appraisal_menu_views.xml',
        'views/appraisal_views.xml',
        'views/appraisal_note_views.xml',
        'views/res_config_settings_views.xml',
        'views/appraisal_goal_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_appraisal_goal_tag_views.xml',
        'views/hr_department_views.xml',
        'wizard/request_appraisal_views.xml',
        'wizard/appraisal_ask_feedback_views.xml',
        'report/appraisal_analysis_report_view.xml',
    ],
    'installable': True,
    'application': True,
    "maintainer": "Aspire Softserv Pvt. Ltd",
    "support": "odoo@aspiresoftserv.com",
}
