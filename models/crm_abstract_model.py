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

    state = fields.Many2one('crm.states.product', string='Trạng thái', default=_default_stage,
                            track_visibility='always', group_expand='_read_group_stage_ids', store=True)

    sequence = fields.Integer(string='Số TT', readonly=True,
                              force_save=True, track_visibility='always', index=True)
    requirement = fields.Selection(string='Nhu cầu', selection=[(
        'rental', 'Cho thuê'), ('sale', 'Cần bán')], track_visibility='always',)
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

    def _compute_show_data(self):
        pass

    def _get_suppoter_ids(self):
        pass

    def _get_default_employee_id(self):
        return self.env['hr.employee'].search([
            ('user_id', '=', self.env.user.id)
        ]).id


class CrmRequestRuleAbstractModel(models.AbstractModel):
    _name = 'crm.request.rule.abstract.model'
    _description = 'CRM Request Rule Abstract Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Tên', default='New', readonly=True, force_save=True, track_visibility='always')
    requirement = fields.Selection(string='Nhu cầu', selection=[('rental','Cho thuê'),('sale','Cần bán')], track_visibility='always')
    employee_id = fields.Many2one('hr.employee','CV chăm sóc',ondelete='cascade')
    approver = fields.Many2one('hr.employee', 'Người duyệt')
    state = fields.Selection(string='Trạng thái', selection=[('draft','Chưa duyệt'),('approved','Đã duyệt'),('cancel','Từ chối'), ('closed','Đóng')], default="draft")
    approved_date = fields.Datetime(string='Ngày duyệt')