# -*- coding: utf-8 -*-

import json
import logging

from odoo import _, api, fields, models, registry, exceptions
from odoo.exceptions import UserError
from odoo.tools.translate import _
from odoo.addons import decimal_precision as dp
from ..commons.bds_constant import *
from datetime import datetime


class CrmProductReuqestRule(models.Model):
    _name = 'crm.product.request.rule'
    _description = 'CRM Product Request Rule'
    _inherit = 'crm.request.rule.abstract.model'

    def get_default_product(self):
        return self.env.context.get('default_product', False)

    crm_product_id = fields.Many2one(
        'crm.product', 'CRM Product', ondelete='cascade', default=get_default_product)
    crm_request_sheet_id = fields.Many2one(
        'crm.product.request.rule.sheet', 'Sheet')
    is_show_attachment = fields.Boolean(
        'Xem hình ảnh', default=True, readonly=True, force_save=True)
    is_show_house_no = fields.Boolean(
        'Xem số nhà', default=True, readonly=True, force_save=True)
    is_show_map = fields.Boolean(
        'Xem bản đồ', default=True, readonly=True, force_save=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'crm.product.request.rule') or '/'
            vals['sequence'] = int(vals['name'].split('-')[1])
        res = super().create(vals)
        return res

    @api.onchange('requirement')
    def _domain_employee(self):
        domain = []
        if self.requirement == 'sale':
            user_sale_group_id = self.env.ref('bds.crm_product_sale_user').id
            domain = [
                ('user_id.groups_id', '=', user_sale_group_id)
            ]
        else:
            user_rental_group_id = self.env.ref(
                'bds.crm_product_rental_user').id
            domain = [
                ('user_id.groups_id', '=', user_rental_group_id)
            ]
        return {
            'domain': {
                'employee_id': domain
            }
        }


class CrmProductReuqestRuleSheet(models.Model):
    _name = 'crm.product.request.rule.sheet'
    _description = 'CRM Product Request Rule Sheet'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Tên', default='New', readonly=True,
                       force_save=True, track_visibility='always')
    employee_id = fields.Many2one('hr.employee', 'CV chăm sóc', ondelete='cascade',
                                  default=lambda self: self._get_default_employee_id())
    crm_request_line_ids = fields.One2many(
        comodel_name='crm.product.request.rule', inverse_name="crm_request_sheet_id", string='CV chăm sóc')
    state = fields.Selection(string='Trạng thái', selection=[(
        'draft', 'Chưa duyệt'), ('approved', 'Đã duyệt'), ('cancel', 'Từ chối')], default="draft")
    requirement = fields.Selection(string='Nhu cầu', selection=[(
        'rental', 'Cho thuê'), ('sale', 'Cần bán')], compute='_set_requirement', store=True)
    mail_ids = fields.Many2many(
        comodel_name='mail.activity', string='Mail Activity')
    approver = fields.Many2one('hr.employee', 'Người duyệt')
    approved_date = fields.Datetime(string='Ngày duyệt')

    def _get_url(self):
        return self.env['ir.config_parameter'].sudo().get_param('web.base.url')

    @api.depends('crm_request_line_ids')
    def _set_requirement(self):
        for rec in self:
            sale_count = len(rec.crm_request_line_ids.filtered(
                lambda r: r.requirement == 'sale').ids)
            rental_count = len(rec.crm_request_line_ids.filtered(
                lambda r: r.requirement == 'rental').ids)
            if sale_count and rental_count:
                raise exceptions.VallidationError(
                    'Không thể chọn 2 yêu cầu cho thuê và bán trong cùng 1 bảng xin phân quyền.')
            elif sale_count and rental_count == 0:
                rec.requirement = 'sale'
            else:
                rec.requirement = 'rental'

    def _get_default_employee_id(self):
        return self.env['hr.employee'].search([
            ('user_id', '=', self.env.user.id)
        ]).id

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        context = self.env.context.copy()
        if context.get('active_ids', False) and context.get('active_model', '') == 'crm.product':
            product_lines = []
            ids = context.get('active_ids')
            for _id in ids:
                crm_request_line_value = self._prepare_crm_request_line(
                    self.env['crm.product'].browse(_id))
                product_lines.append((0, 0, crm_request_line_value))
            self.crm_request_line_ids = product_lines

    def _prepare_crm_request_line(self, crm_product_id):
        return {
            'employee_id': self.employee_id.id,
            'crm_product_id': crm_product_id.id,
            'requirement': crm_product_id.requirement,
            'is_show_attachment': True,
            'is_show_house_no': True,
            'is_show_map': True
        }

    def send_notification_request(self):
        requirement = self.requirement
        groups_id = []
        groups_id.append(self.env.ref('bds.crm_product_manager').id)
        if requirement == 'sale':
            groups_id.append(self.env.ref('bds.crm_product_sale_manager').id)
            # groups_id.append(self.env.ref('bds.crm_product_sale_user_view_all').id)
        else:
            groups_id.append(self.env.ref('bds.crm_product_rental_manager').id)
            # groups_id.append(self.env.ref('bds.crm_product_rental_user_view_all').id)
        user_ids = self.env['res.users'].search([
            ('groups_id', 'in', groups_id)
        ])
        mail_ids = []
        for user in user_ids:
            res = self._create_email_activity(user)
            mail_ids.append(res.id)
        self.update({
            'mail_ids': [(6, 0, mail_ids)]
        })

    def make_action_done(self):
        for mail in self.mail_ids:
            mail.action_done()

    @api.multi
    def btn_save(self):
        self.send_notification_request()
        context = self.env.context.copy()
        context['default_message'] = 'Yêu cầu phân quyền đã được gửi. Vui lòng chờ phản hồi từ cấp cao hơn'
        return {
            'name': 'Xin phân quyền',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'announce',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
            'res_id': False,
        }

    @api.multi
    def btn_approve(self):
        self.ensure_one()
        approver = self.env.user.employee_ids[0]
        self.update({
            'state': 'approved',
            'approved_date': datetime.now(),
            'approver': approver.id
        })
        request_rule = self.env['crm.product.request.rule']
        self._set_all_previous_approved_to_close()
        for line in self.crm_request_line_ids:
            existed_line_id = request_rule.search([
                ('employee_id', '=', line.employee_id.id),
                ('crm_product_id', '=', line.crm_product_id.id),
                ('state', '=', 'approved')
            ])
            if existed_line_id.id:
                existed_line_id.write({
                    'state': 'closed',
                })
            line.write({
                'state': 'approved',
                'approved_date': datetime.now(),
                'approver': approver.id
            })
        self.make_action_done()
        self.send_notification('Đã duyệt bởi: {}'.format(approver.name))

    def _remove_mail_activity(self):
        for mail in self.mail_ids:
            mail.unlink()

    @api.multi
    def btn_reject(self):
        approver = self.env.user.employee_ids[0]
        self.write({
            'state': 'cancel',
            'approved_date': datetime.now(),
            'approver': approver.id
        })
        self.crm_request_line_ids.write({
            'state': 'cancel',
            'approved_date': datetime.now(),
            'approver': approver.id
        })
        self._remove_mail_activity()
        self.send_notification('Từ chối bởi: {}'.format(approver.name))

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'crm.product.request.rule.sheet') or '/'
            vals['sequence'] = int(vals['name'].split('-')[1])
        res = super().create(vals)
        return res

    def _create_email_activity(self, user_id):
        model_id = self.env['ir.model'].search(
            [('model', '=', self._name)]).id
        activity_type_id = self.env.ref('mail.mail_activity_data_todo').id
        summary = 'Yêu cầu phần quyền từ {}'.format(self.employee_id.name)
        date_deadline = fields.Date.today()
        note = 'Yêu cầu duyệt phân quyền từ {}'.format(self.employee_id.name)
        user_id = user_id.id
        vals = {
            'activity_type_id': activity_type_id,
            'summary': summary,
            'date_deadline': date_deadline,
            'note': note,
            'res_id': self.id,
            'res_model_id': model_id,
            'user_id': user_id
        }
        res = self.env['mail.activity'].create(vals)
        return res

    def _get_url(self):
        return self.env['ir.config_parameter'].sudo().get_param('web.base.url')

    def send_notification(self, msg):
        user = self.employee_id.user_id
        message = BODY_MSG.format(self._get_url(
        ), user.partner_id.id, user.partner_id.id, user.partner_id.name, msg)
        self.message_post(body=message, message_type="comment",
                          partner_ids=[user.partner_id.id])

    def _set_all_previous_approved_to_close(self):
        product_ids = self.crm_request_line_ids.mapped(
            lambda r: r.crm_product_id)
        for product in product_ids:
            product.supporter_with_rule_ids.filtered(
                lambda r: r.state == 'approved').write({'state': 'closed'})
