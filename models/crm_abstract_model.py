# -*- coding: utf-8 -*-

# Import libs
import json
import logging
from lxml import etree
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
    description = fields.Text('Diễn giải',compute='_set_description',store=True)

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
        comodel_name='hr.employee', string='CV môi giới', default=lambda self: self._get_default_employee_id(), track_visibility='always')
    supporter_ids = fields.Many2many(comodel_name='hr.employee', string='CV chăm sóc', compute="_get_suppoter_ids",store=True)
    is_manager = fields.Boolean('Là Manager',compute='_is_manager')
    # is_duplicate_phone_1 = fields.Boolean('Trùng số 1', compute='_duplicate_phone_num', store=True)
    # is_duplicate_phone_2 = fields.Boolean('Trùng số 2', compute='_duplicate_phone_num', store=True)
    # is_duplicate_phone_3 = fields.Boolean('Trùng số 3', compute='_duplicate_phone_num', store=True)
    is_duplicate_phone_1 = fields.Boolean('Trùng số 1', default=False)
    is_duplicate_phone_2 = fields.Boolean('Trùng số 2', default=False)
    is_duplicate_phone_3 = fields.Boolean('Trùng số 3', default=False)

    @api.constrains('is_duplicate_phone_1','is_duplicate_phone_2','is_duplicate_phone_3')
    def _constrains_phone_number(self):
        for rec in self:
            if rec.is_duplicate_phone_1 or rec.is_duplicate_phone_2 or rec.is_duplicate_phone_3:
                raise exceptions.ValidationError('Trùng số điện thoại, không thể lưu')

    @api.depends('name')
    def _is_readonly_requirement(self):
        for rec in self:
            rec.readonly_requirement = True
            user = self.env.user
            if user.has_group('bds.crm_request_manager') or user.has_group('bds.crm_product_manager'):
                rec.readonly_requirement = False

    def _is_manager(self):
        pass

    def _set_description(self):
        pass

    def _compute_show_data(self):
        pass

    def _get_suppoter_ids(self):
        pass

    def _get_default_employee_id(self):
        return self.env['hr.employee'].search([
            ('user_id', '=', self.env.user.id)
        ]).id

    def _check_duplicate_phone_number_in_record(self):
        """Kiểm tra 3 số điện thoại của chủ nhà có bị trùng hay không

        Returns:
            [type] -- [description]
        """
        is_duplicate_phone_1 = False
        is_duplicate_phone_2 = False
        is_duplicate_phone_3 = False
        if self.host_number_1 == self.host_number_2:
            is_duplicate_phone_1 = is_duplicate_phone_2 = True
        if self.host_number_1 == self.host_number_3:
            is_duplicate_phone_1 = is_duplicate_phone_3 = True
        if self.host_number_2 == self.host_number_3:
            is_duplicate_phone_2 = is_duplicate_phone_3 = True
        if self.host_number_2 == self.host_number_1:
            is_duplicate_phone_2 = is_duplicate_phone_1 = True
        if self.host_number_3 == self.host_number_1:
            is_duplicate_phone_3 = is_duplicate_phone_1 = True
        if self.host_number_3 == self.host_number_2:
            is_duplicate_phone_3 = is_duplicate_phone_2 = True
        return is_duplicate_phone_1,is_duplicate_phone_2,is_duplicate_phone_3
    
    @api.onchange('host_number_1','host_number_2','host_number_3')
    def _duplicate_phone_num(self):
        for rec in self:
            is_duplicate_phone_1 = False
            is_duplicate_phone_2 = False
            is_duplicate_phone_3 = False
            if rec.host_number_1 and rec.host_number_1 != rec._origin.host_number_1 and rec.host_number_2 and rec.host_number_2 != rec._origin.host_number_2 and rec.host_number_3 and rec.host_number_3 != rec._origin.host_number3:
                is_duplicate_phone_1, is_duplicate_phone_2, is_duplicate_phone_3 = rec._check_duplicate_phone_number_in_record()
                _li_phone_data = []
                if rec.requirement == 'sale':
                    #Query phone number form crm product
                    _li_phone_sale_tmp = self.env['crm.product'].search([
                        ('requirement','=','sale')
                    ]).mapped(lambda r: [r.host_number_1,r.host_number_2,r.host_number_3])
                    for i in _li_phone_sale_tmp:
                        _li_phone_data += i

                    #Query phone number form crm request
                    _li_phone_sale_tmp = self.env['crm.request'].search([
                        ('requirement','=','sale')
                    ]).mapped(lambda r: [r.host_number_1,r.host_number_2,r.host_number_3])                
                    
                    for i in _li_phone_sale_tmp:
                        _li_phone_data += i
                else:
                    #Query phone number form crm product
                    _li_phone_sale_tmp = self.env['crm.product'].search([
                        ('requirement','=','rental')
                    ]).mapped(lambda r: [r.host_number_1,r.host_number_2,r.host_number_3])
                    for i in _li_phone_sale_tmp:
                        _li_phone_data += i

                    #Query phone number form crm request
                    _li_phone_sale_tmp = self.env['crm.request'].search([
                        ('requirement','=','rental')
                    ]).mapped(lambda r: [r.host_number_1,r.host_number_2,r.host_number_3])
                    for i in _li_phone_sale_tmp:
                        _li_phone_data += i
                #Validate data
                if rec.host_number_1 in _li_phone_data:
                    is_duplicate_phone_1 = True
                if rec.host_number_2 in _li_phone_data:
                    is_duplicate_phone_2 = True
                if rec.host_number_3 in _li_phone_data:
                    is_duplicate_phone_3 = True
            rec.is_duplicate_phone_1 = is_duplicate_phone_1
            rec.is_duplicate_phone_2 = is_duplicate_phone_2
            rec.is_duplicate_phone_3 = is_duplicate_phone_3


    def _get_url(self):
        return self.env['ir.config_parameter'].sudo().get_param('web.base.url')
    
    # def _update_state(self,state_id):
    #     self.write({
    #         'state': state_id.id
    #     })
    #     context = self.env.context.copy()
    #     context['default_message'] = 'Đã chuyển trạng thái sang: "{}"'.format(state_id.name)
    #     view_id = self.env.ref('bds.announcement_change_state').id
    #     return {
    #         'name': 'Đã chuyển trạng thái',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'view_id': view_id,
    #         'res_model': 'ecc.approval.role',
    #         'context': context,
    #         'target': 'new',
    #         'type': 'ir.actions.act_window',
    #     }

    # @api.multi
    # def btn_draft(self):
    #     self.ensure_one()
    #     state_id = self.env.ref('bds.crm_state_draft')
    #     return self._update_state(state_id)
        

    # @api.multi
    # def btn_for_sale(self):
    #     self.ensure_one()
    #     state_id = self.env.ref('bds.crm_state_open')
    #     return self._update_state(state_id)

    # @api.multi
    # def btn_stop_sale(self):
    #     self.ensure_one()
    #     state_id = self.env.ref('bds.crm_state_stop')
    #     return self._update_state(state_id)

    # @api.multi
    # def btn_pending(self):
    #     self.ensure_one()
    #     state_id = self.env.ref('bds.crm_state_pending')
    #     return self._update_state(state_id)

    # @api.multi
    # def btn_trade_completed(self):
    #     self.ensure_one()
    #     state_id = self.env.ref('bds.crm_state_done')
    #     return self._update_state(state_id)

    # @api.multi
    # def btn_ontrade(self):
    #     self.ensure_one()
    #     state_id = self.env.ref('bds.crm_state_ongoing')
    #     return self._update_state(state_id)


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
