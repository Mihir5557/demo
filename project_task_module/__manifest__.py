# -*- coding: utf-8 -*-
###############################################################################
#
# Aspire Softserv Pvt. Ltd.
# Copyright (C) Aspire Softserv Pvt. Ltd.(<https://aspiresoftserv.com>).
#
###############################################################################
{
    "name": "Project Task Modules",
    "category": "Project Management",
    "summary": "Project Task Modules",
    "version": "18.0.0.1.0",
    "license": "AGPL-3",
    'description': """
                This module adds a new field 'Project Module' in Project Tasks. This helps bifurcating tasks by project modules. 
              User can filter/group tasks by module. This makes Kanban view clean and compact.
    """,
    "author": "Aspire Softserv Pvt. Ltd",
    "website": "https://aspiresoftserv.com",
    "depends": ["project"],
    "data": [
        "security/ir.model.access.csv",
        "views/project_task.xml",
        "views/project_view.xml"
    ],
    "application": True,
    "installable": True,
    "maintainer": "Aspire Softserv Pvt. Ltd",
    "support": "odoo@aspiresoftserv.com",
}
