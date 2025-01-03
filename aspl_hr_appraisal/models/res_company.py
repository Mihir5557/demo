# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = "res.company"

    def _get_default_employee_feedback_template(self):
        return """
    <h2>
            <span style="font-weight: bolder;">
                My work
            </span>
        </h2>
        <h3>What are my best achievement(s) since my last appraisal?</h3>
        <p>
            <em>
                Describe something that made you proud, a piece of work positive for
                the company.
            </em>
        </p>
        <p>
            <br/>
        </p>
        <h3>
            What has been the most challenging aspect of my work this past year and
            why?
        </h3>
        <p>
            <em>
                Did you face new difficulties? Did you confront yourself to new
                obstacles?
            </em>
        </p>
        <p>
            <br/>
        </p>
        <h3>What would I need to improve my work?</h3>
        <p>
            <em>
                How can the company help you with your need and objectives in order
                for you to reach your goals and look for the best collaboration.
            </em>
        </p>
        <p>
            <br/>
        </p>
        <h2>
            <span style="font-weight: bolder;">
                My future
            </span>
        </h2>
        <h3>
            What are my short and long-term goals with the company, and for my
            career?
        </h3>
        <ul>
            <li>
                <em>Give an example of short-term objective (&lt; 6 months)</em>
            </li>
        </ul>
        <p>
            <br/>
        </p>
        <ul>
            <li>
                <em>Give an example of long-term objective (&gt; 6 months)</em>
            </li>
        </ul>
        <p>
            <br/>
        </p>
        <h3>Which parts of my job do I most / least enjoy?</h3>
        <p>
            <em>
                Every job has strong points, what are, in your opinion, the tasks that
                you enjoy the most/the least?
            </em>
        </p>
        <p>
            <br/>
        </p>
        <h2>
            <span style="font-weight: bolder;">
                My feelings
            </span>
        </h2>
        <h3>How do I feel about the company...</h3>
        <ul>
            <li>
                <em>Culture/Behavior:</em>
                <span class="o_stars o_five_stars" id="checkId-1">
                    <i class="fa fa-star-from dateutil.relativedelta import relativedelta
o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i>
                </span>
            </li>
            <li>
                <em>Internal Communication:</em>
                <span class="o_stars o_five_stars" id="checkId-2">
                    <i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i>
                </span>
            </li>
        </ul>
        <h3>How do I feel about my own...</h3>
        <ul>
            <li>
                <em>Job's content:</em>
                <span class="o_stars o_five_stars" id="checkId-3">
                    <i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i>
                </span>
            </li>
            <li>
                <em>Work organization:</em>
                <span class="o_stars o_five_stars" id="checkId-4">
                    <i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i>
                </span>
            </li>
            <li>
                <em>Remuneration:</em>
                <span class="o_stars o_five_stars" id="checkId-5">
                    <i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i>
                </span>
            </li>
        </ul>
    """

    def _get_default_manager_feedback_template(self):
        return """
    <h2>
                    <span style="font-weight: bolder;">
                        Feedback
                    </span>
                </h2>
                <h3>
                    Give one positive achievement that convinced you of the employee's
                    value.
                </h3>
                <p>
                    <em>
                        Some achievements comforting you in their strengths to face job's
                        issues.
                    </em>
                </p>
                <p>
                    <br/>
                </p>
                <h2>
                    <span style="font-weight: bolder;">
                        Evaluation
                    </span>
                </h2>
                <p>
                    <br/>
                </p>
                <table class="table table-bordered o_table" style="width: 268.656px;">
                    <tbody>
                        <tr>
                            <td style="width: 172.656px;">
                                <p>
                                    <em>Stress Resistance</em>
                                </p>
                            </td>
                            <td style="width: 95px;">
                                <span class="o_stars o_five_stars" id="checkId-6">
                                <i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i>
                                </span>
                            </td>
                        </tr>
                        <tr>
                            <td style="width: 314.078px;">
                                <p>
                                    <em>Time Management</em>
                                </p>
                            </td>
                            <td style="width: 314.078px;">
                                <span class="o_stars o_five_stars" id="checkId-7">
                                    <i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i>
                                </span>
                            </td>
                        </tr>
                        <tr>
                            <td style="width: 314.078px;">
                                <p>
                                    <em>Teamwork</em>
                                </p>
                            </td>
                            <td style="width: 314.078px;">
                                <span class="o_stars o_five_stars" id="checkId-8">
                                    <i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i>
                                </span>
                            </td>
                        </tr>
                        <tr>
                            <td style="width: 314.078px;">
                                <p>
                                    <em>Autonomy</em>
                                </p>
                            </td>
                            <td style="width: 314.078px;">
                                <span class="o_stars o_five_stars" id="checkId-9">
                                <i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i>
                                </span>
                            </td>
                        </tr>
                        <tr>
                            <td style="width: 314.078px;">
                                <p>
                                    <em>Pro-activity</em>
                                </p>
                            </td>
                            <td style="width: 314.078px;">
                                <span class="o_stars o_five_stars" id="checkId-10">
                                    <i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i><i class="fa fa-star-o" contenteditable="false"></i>
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <p>
                    <br/>
                </p>
                <h2>
                    <span style="font-weight: bolder;">
                        Improvements
                    </span>
                </h2>
                <h3>How could the employee improve?</h3>
                <p>
                    <em>
                        From a manager point of view, how could you help the employee to
                        overcome their weaknesses?
                    </em>
                </p>
                <p>
                    <br/>
                </p>
                <h3>Short term (6-months) actions / decisions / objectives</h3>
                <p>
                    <em>Do you need rapid answer to the current situation?</em>
                </p>
                <p>
                    <br/>
                </p>
                <h3>
                    Long term (&gt; 6 months) career discussion, where does the employee
                    wants to go, how to help them reach this path?
                </h3>
                <p>
                    <em>
                        How do you see the employee in the future, do your vision follow the
                        employee's desire?
                    </em>
                </p>
                <p>
                    <br/>
                </p>
            """

    def _get_default_appraisal_survey_template_id(self):
        return self.env.ref('hr_appraisal_survey.appraisal_feedback_template', raise_if_not_found=False)

    appraisal_survey_template_id = fields.Many2one('survey.survey')
    hr_appraisal_plan = fields.Boolean(string='Automatically Generate Appraisals', default=True)
    assessment_note_ids = fields.One2many('appraisal.note', 'company_id')
    send_feedback_employee = fields.Html(default=_get_default_employee_feedback_template)
    send_feedback_manager = fields.Html(default=_get_default_manager_feedback_template)
    duration_after_recruitment = fields.Integer(string="Create an Appraisal after recruitment", default=6)
    month_first = fields.Integer(string="Create a first Appraisal after", default=6)
    month_next = fields.Integer(string="Create a second Appraisal after")
