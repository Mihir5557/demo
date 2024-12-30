# See LICENSE file for full copyright and licensing details.

from odoo.tests import common


class ProjectProjectTestCase(common.TransactionCase):
    def setup(self):
        super(ProjectProjectTestCase, self).setup()

    def test_project_action(self):
        user_root = self.env.ref('base.user_root')
        user_demo = self.env.ref('base.user_demo')

        team = self.env['crm.team'].create({
            'name': 'Test Project Team',
            'user_id': user_root.id,
            'type_team': 'sale',
            'team_members': [(6, 0, [user_root.id, user_demo.id])]
        })

        project = self.env['project.project'].create({
            'name': 'Test Project',
            'team_id': team.id
        })

        team_members = project.get_team_members()

        self.assertTrue(user_root.id in team_members, f"User {user_root.name} should be a team member.")
        self.assertTrue(user_demo.id in team_members, f"User {user_demo.name} should be a team member.")

