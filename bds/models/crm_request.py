# -*- coding: utf-8 -*-

import json
import logging

from odoo import _, api, fields, models, registry
from odoo.exceptions import UserError
from odoo.tools.translate import _
from odoo.addons import decimal_precision as dp
from ..commons.bds_constant import *
from datetime import datetime

_logger = logging.getLogger(__name__)



class CrmRequest(models.Model):
    _name = 'crm.request'
    _description = 'CRM Request'
    _inherit = 'crm.abstract.model'


    name = fields.Char(string='Số đăng ký', default='New',
                       readonly=True, force_save=True, track_visibility='always')
    customer_uid = fields.Char(string='Mã KH',track_visibility='always',compute='_set_customer_uid',store=True)
    email = fields.Char('Email')
    financial_capability = fields.Float('Khả năng tài chính', digits=dp.get_precision(
        'Product Price'), track_visibility='always')
    currency = fields.Selection(string='Tiền tệ',selection=[('usd','$'),('mil','Triệu'),('bil','Tỷ')])
    zone = fields.Char('Khu vực hoạt động', track_visibility='always')
    business_demand = fields.Selection(string='Nhu cầu KD',selection=NCKD)
    
    is_show_email = fields.Boolean('Show Email', compute='_compute_show_data')
    supporter_with_rule_ids = fields.One2many(comodel_name='crm.request.request.rule', inverse_name="crm_product_id", string='CV chăm sóc và phân quyền', track_visibility='always',
                                              domain=[('state', '=', 'approved')], ondelete='cascade',
                                              readonly=True, force_save=True)
    supporter_full_ids = fields.One2many(comodel_name='crm.request.request.rule', inverse_name="crm_product_id", string='Phân quyền',
                                         groups='bds.crm_request_change_rule_user,bds.crm_request_manager', ondelete='cascade')
    

    #Field for description
    way = fields.Char('Tập trung tuyến đường')
    rental_price = fields.Char('Giá cho thuê',)
    dientich = fields.Char('Diện tích dao động')
    min_horizontal = fields.Char('Ngang tối thiểu')
    parking_lot = fields.Char('Chỗ để xe')
    partner_kd = fields.Char('Chủ KD hiện tại')
    note = fields.Text('Ghi chú')
    source = fields.Char('Nguồn')
    potential_evaluation = fields.Char('Đánh giá tiềm năng')


    @api.depends('partner_kd','potential_evaluation','note','source','type_of_real_estate','type_of_road','zone','business_demand','way','rental_price','dientich','min_horizontal','parking_lot')
    def _set_description(self):
        description = 'Khách hàng cần thuê {loaibds}  - {loaiduong} - {khuvuc}, nhu cầu kinh doanh: {nckd}. Tập trung tuyến đường {way}. \
            Giá thuê dao động: {gia}.Cần diện tích dao động: {dientich} - Ngang tối thiểu: {min}, Cần chỗ để xe khoảng: {dexe}. \
            Hiện đang là chủ kinh doanh: {ckd}. Đánh giá mức độ tiềm năng: {danhgia}. Ghi chú: {note}. Nguồn: {nguon}'
        description = description.format(loaibds=self.type_of_real_estate, loaiduong=self.type_of_road, khuvuc=self.zone,nckd=self.business_demand,\
            way=self.way,gia=self.rental_price,dientich=self.dientich, min=self.min_horizontal, dexe=self.parking_lot,\
                ckd=self.partner_kd,danhgia=self.potential_evaluation,note=self.note,nguon=self.source)
        return description

    @api.depends('name')
    def _is_manager(self):
        current_user = self.env.user
        for rec in self:
            is_manager = False
            if current_user.has_group('bds.crm_request_manager') \
            or current_user.has_group('bds.crm_request_rental_manager') or current_user.has_group('bds.crm_request_sale_manager'):
                is_manager = True
            rec.is_manager = is_manager

    @api.depends('name')
    def _set_customer_uid(self):
        for rec in self:
            rec.customer_uid = rec.name


    @api.depends('supporter_with_rule_ids')
    def _compute_show_data(self):
        current_user = self.env.user
        for rec in self:
            rec.is_brokerage_specialist = False
            if current_user.has_group('bds.crm_request_manager') \
                    or current_user.has_group('bds.crm_request_rental_manager') or current_user.has_group('bds.crm_request_sale_manager'):
                rec.is_brokerage_specialist = True
            elif rec.brokerage_specialist.user_id == current_user \
                or current_user.has_group('bds.crm_request_sale_user_view_all')\
                     or current_user.has_group('bds.crm_request_rental_user_view_all'):
                rec.is_show_attachment = True
                rec.is_show_email = True
            else:
                employee_id = rec.supporter_with_rule_ids.filtered(
                    lambda r: r.employee_id.user_id == current_user and r.state == 'approved')
                rec.is_show_attachment = employee_id.is_show_attachment
                rec.is_show_email = employee_id.is_show_email
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') != '':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'crm.request') or '/'
        res = super().create(vals)
        return res

    @api.multi
    def btn_request_rule(self):
        self.ensure_one()
        view_id = self.env.ref(
            'bds.crm_request_request_rule_sheet_view_form_wizard').id
        return {
            'name': 'Xin phân quyền',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'res_model': 'crm.request.request.rule.sheet',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': False,
        }
