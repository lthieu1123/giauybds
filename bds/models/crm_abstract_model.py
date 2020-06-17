# -*- coding: utf-8 -*-

# Import libs
import json
import logging
from odoo import SUPERUSER_ID
from odoo import api, fields, models, exceptions
from odoo.tools.translate import _
from odoo.addons import decimal_precision as dp
from ..commons.bds_constant import *


class CrmAbstractModel(models.AbstractModel):
    _name = 'crm.abstract.model'
    _description = 'Crm Abstract Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def _default_stage(self):
        return self.env['crm.states.product'].search([], limit=1, order='sequence').id

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        return self.env['crm.states.product'].search([])

    def _get_default_requirement(self):
        user = self.env.user
        if user.has_group('bds.crm_product_rental_manager') \
            or user.has_group('bds.crm_request_rental_manager') \
            or user.has_group('bds.crm_product_rental_user') \
            or user.has_group('bds.crm_request_rental_user'):
            return 'rental'
        elif user.has_group('bds.crm_request_sale_user') \
            or user.has_group('bds.crm_product_sale_user') \
            or user.has_group('bds.crm_request_sale_manager') \
            or user.has_group('bds.crm_product_sale_manager'):
            return 'sale'
        else:
            return False
    
    readonly_requirement = fields.Boolean('readonly_requirement',compute='_is_readonly_requirement')
    state = fields.Many2one('crm.states.product', string='Trạng thái', default=_default_stage,
                            track_visibility='always', group_expand='_read_group_stage_ids', store=True)

    sequence = fields.Integer(string='Số TT', readonly=True,
                              force_save=True, track_visibility='always', index=True)
    requirement = fields.Selection(string='Nhu cầu', selection=[(
        'rental', 'Cho thuê'), ('sale', 'Cần bán')], track_visibility='always', default=_get_default_requirement)
    type_of_real_estate = fields.Selection(
        string='Loại BĐS', selection=TYPE_OF_REAL_ESTATE, required=True, track_visibility='always')
    direction = fields.Selection(
        string='Hướng', selection=CARDINAL_DIRECTION, track_visibility='always')
    description = fields.Text('Diễn giải')

    host_name = fields.Char('Tên chủ', track_visibility='always')
    host_number_1 = fields.Char('Số ĐT 1')
    host_number_2 = fields.Char('Số ĐT 2')
    host_number_3 = fields.Char('Số ĐT 3')

    is_show_attachment = fields.Boolean(
        'Xem hình ảnh', compute="_compute_show_data")
    is_show_house_no = fields.Boolean(
        'Xem số nhà', compute="_compute_show_data")
    is_brokerage_specialist = fields.Boolean(
        'Là chủ hồ sơ', compute="_compute_show_data")

    brokerage_specialist = fields.Many2one(
        'hr.employee', 'CV môi giới', default=lambda self: self._get_default_employee_id(), track_visibility='always')
    supporter_ids = fields.Many2many(
        'hr.employee', 'CV môi giới', compute="_get_suppoter_ids")

    @api.depends('name')
    def _is_readonly_requirement(self):
        for rec in self:
            rec.readonly_requirement = True
            user = self.env.user
            if user.has_group('bds.crm_request_manager') or user.has_group('bds.crm_product_manager'):
                rec.readonly_requirement = False
            

    def _compute_show_data(self):
        pass

    def _get_suppoter_ids(self):
        pass

    def _get_default_employee_id(self):
        return self.env['hr.employee'].search([
            ('user_id', '=', self.env.user.id)
        ]).id

    def _check_constrains_phone_number(self):
        """Kiểm tra 3 số điện thoại của chủ nhà có bị trùng hay không

        Returns:
            [type] -- [description]
        """
        _li_phone_no = [i for i in [self.host_number_1,
                                    self.host_number_2, self.host_number_3] if i]
        return len(_li_phone_no) == len(set(_li_phone_no))

    @api.constrains('host_number_1', 'host_number_2', 'host_number_3')
    def _constrains_phone_number(self):
        for rec in self:
            res = rec._check_constrains_phone_number()
            if not res:
                raise exceptions.ValidationError(
                    'Số điện thoại bị trùng. Vui lòng nhập lại')

    @api.onchange('host_number_1', 'host_number_2', 'host_number_3')
    def _onchange_phone_number(self):
        res = self._check_constrains_phone_number()
        if not res:
            raise exceptions.ValidationError(
                'Số điện thoại bị trùng. Vui lòng nhập lại')


class CrmRequestRuleAbstractModel(models.AbstractModel):
    _name = 'crm.request.rule.abstract.model'
    _description = 'CRM Request Rule Abstract Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Tên', default='New', readonly=True,
                       force_save=True, track_visibility='always')
    requirement = fields.Selection(string='Nhu cầu', selection=[(
        'rental', 'Cho thuê'), ('sale', 'Cần bán')], track_visibility='always')
    employee_id = fields.Many2one(
        'hr.employee', 'CV chăm sóc', ondelete='cascade')
    approver = fields.Many2one('hr.employee', 'Người duyệt')
    state = fields.Selection(string='Trạng thái', selection=[('draft', 'Chưa duyệt'), (
        'approved', 'Đã duyệt'), ('cancel', 'Từ chối'), ('closed', 'Đóng')], default="draft")
    approved_date = fields.Datetime(string='Ngày duyệt')
