# -*- coding: utf-8 -*-
###############################################################################
#
# Aspire Softserv Pvt. Ltd.
# Copyright (C) Aspire Softserv Pvt. Ltd.(<https://aspiresoftserv.com>).
#
###############################################################################
{
    "name": "Project Timesheet Activity",
    "category": "Timesheet",
    "version": "18.0.0.1.0",
    "summary": "his module adds a new field 'Activity' in timesheet line. User can analyze the time spent in different type of activities. This analysis helps in better planning.",
    "license": "AGPL-3",
    "author": "Aspire Softserv Pvt. Ltd",
    "website": "https://aspiresoftware.in",
    "depends": ['hr_timesheet',
                'project',
                ],
    "data": [
        "security/ir.model.access.csv",
        "views/project_timesheet_activity_configuration_views.xml",
        "views/project_task_views.xml",
        "wizards/move_timesheet_entry.xml",
    ],
    "application": False,
    "installable": True,
    "maintainer": "Aspire Softserv Pvt. Ltd",
    "support": "odoo@aspiresoftserv.com",
}
