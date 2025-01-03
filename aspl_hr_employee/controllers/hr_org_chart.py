# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.http import request

from odoo import http
from odoo.addons.hr_org_chart.controllers.hr_org_chart import HrOrgChartController


class HrOrgChartControllerExtend(HrOrgChartController):

    def _prepare_employee_data(self, employee):
        job = employee.sudo().job_id
        return dict(
            id=employee.id,
            name=employee.name,
            link='/mail/view?model=%s&res_id=%s' % ('hr.employee.public', employee.id,),
            job_id=job.id,
            job_name=job.name or '',
            job_title=employee.job_title or '',
            direct_sub_count=len(employee.child_ids.employee_id.filtered(lambda x: x.with_organization) - employee.employee_id.filtered(lambda x: x.with_organization)),
            indirect_sub_count=employee.child_all_count,
        )
        
    @http.route('/hr/get_org_chart', type='json', auth='user')
    def get_org_chart(self, employee_id, **kw):

        employee = self._check_employee(employee_id, **kw)
        if not employee:  # to check
            return {
                'managers': [],
                'children': [],
            }

        # compute employee data for org chart
        ancestors, current = request.env['hr.employee.public'].sudo(), employee.sudo()
        while current.parent_id and len(ancestors) < self._managers_level + 1:
            ancestors += current.parent_id
            current = current.parent_id

        employee_ids = employee.child_ids.employee_id.filtered(lambda x: x.with_organization)
        child_ids = request.env['hr.employee.public'].browse(employee_ids.ids)

        values = dict(
            self=self._prepare_employee_data(employee),
            managers=[
                self._prepare_employee_data(ancestor)
                for idx, ancestor in enumerate(ancestors)
                if idx < self._managers_level
            ],
            managers_more=len(ancestors) > self._managers_level,
            children=[self._prepare_employee_data(child) for child in child_ids],
        )
        values['managers'].reverse()
        return values
    
    
    def get_subordinates(self, employee_id, subordinates_type=None, **kw):
        res = super().get_subordinates(employee_id, subordinates_type=None, **kw)
        if res:
            employee_ids = request.env['hr.employee'].browse(res)
            res = employee_ids.filtered(lambda x:x.with_organization)
            res = res.ids
            
        return res