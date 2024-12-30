# -*- coding: utf-8 -*-
###############################################################################
#
# Aspire Softserv Pvt. Ltd.
# Copyright (C) Aspire Softserv Pvt. Ltd.(<https://aspiresoftserv.com>).
#
###############################################################################
{
    'name': "Aspire Project Task Extension",
    'category': 'Tools',
    'summary': """To Control The Project Module""",
    'version': '18.0.0.1.0',
    'license': 'LGPL-3',
    'description': """This Module set sprint for project tasks.""",
    'author': "Aspire Softserv Pvt Ltd",
    'website': "http://aspiresoftware.co.in",
    'depends': ['base',
                'project',
                'hr',
                'hr_timesheet',
                'project_task_milestone',
                'project_management_sprint',
                ],
    'data': [
        'security/ir.model.access.csv',
        'views/project_task_views.xml',
        'views/task_type_addition_views.xml',
        'views/project_task_kanban_views.xml',
        'views/code_review_category_views.xml',
        'views/task_priority_views.xml',
        'report/project_task_completion_report_views.xml',
    ],
    # 'external_dependencies': {'python': ['api']},  # pip3 install api
    'installable': True,
    'application': True,
    "maintainer": "Aspire Softserv Pvt. Ltd",
    "support": "odoo@aspiresoftserv.com",
}
