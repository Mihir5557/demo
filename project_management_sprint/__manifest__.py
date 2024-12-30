# -*- coding: utf-8 -*-
###############################################################################
#
# Aspire Softserv Pvt. Ltd.
# Copyright (C) Aspire Softserv Pvt. Ltd.(<https://aspiresoftserv.com>).
#
###############################################################################
{
    'name': 'Project Sprint',
    'category': 'Project',
    'summary': """This app adds sprint functionality to the Odoo Project module,
    enabling efficient task management within fixed timeframes.""",
    'version': '18.0.0.1.0',
    'license': 'AGPL-3',
    'description': """This module enables the sprint functionality""",
    "author": "Aspire Softserv Pvt. Ltd",
    "website": "https://aspiresoftserv.com",
    'depends': ['project'],
    'data': [
        'security/ir.model.access.csv',
        'report/project_sprint_report_views.xml',
        'views/project_sprint_views.xml',
        'views/project_project_views.xml',
        'views/project_task_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    "maintainer": "Aspire Softserv Pvt. Ltd",
    "support": "odoo@aspiresoftserv.com",
}
