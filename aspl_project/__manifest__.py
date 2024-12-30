# -*- coding: utf-8 -*-

{
    'name': "Aspire Project Extension",
    'summary': """
    To Control The Project Module
    """,
    'description': """""",
    'author': "Aspire Softserv Pvt Ltd",
    'website': "http://aspiresoftware.co.in",
    'category': 'Tools',
    'version': '18.0.0.0.0',
    'license': 'LGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base', 'project', 'hr', 'hr_timesheet', 'project_task_module', 'project_team',
                'aspl_project_task'],  # deprecated 'hr_timesheet_sheet',
    # always loaded
    'data': [
        'security/new_record_rules.xml',
        'security/milestone_record_rules.xml',
        'security/ir.model.access.csv',
        'views/project_task_type_views.xml',
        'views/project_project_views.xml',
        'views/inherit_project_task_view.xml',
        'views/project_extend.xml',
        'wizards/interchange_task_timesheet.xml',
        
    ],
    # 'external_dependencies': {'python': ['api']},  # pip3 install api
    'installable': True,
    'application': True,
    'auto_install': False,
}
