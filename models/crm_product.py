# -*- coding: utf-8 -*-

import json
import logging

from odoo import _, api, fields, models, registry, exceptions
from odoo.exceptions import UserError
from odoo.tools.translate import _
from odoo.addons import decimal_precision as dp
from ..commons.bds_constant import *
from datetime import datetime

_logger = logging.getLogger(__name__)


class CrmProduct(models.Model):
    _name = 'crm.product'
    _description = 'CRM Product'
    _inherit = 'crm.abstract.model'

    name = fields.Char(string='Số đăng ký', default='New',
                       readonly=True, force_save=True, track_visibility='always')

    # Address
    house_no = fields.Char('Số nhà', required=True)
    ward_no = fields.Many2one('crm.ward', 'Phường/Xã', track_visibility='always',
                              domain="[('district_id','=?',district_id)]", required=True)
    street = fields.Many2one('crm.street', 'Đường', track_visibility='always',
                             domain="[('district_id','=?',district_id)]", required=True)
    country_id = fields.Many2one('res.country', 'Quốc gia', default=lambda self: self.env.ref(
        'base.vn'), track_visibility='always',)
    state_id = fields.Many2one('res.country.state', 'Tỉnh/TP',
                               domain="[('country_id','=',country_id)]", track_visibility='always', default = lambda self: self.env.ref('bds.state_vn_VN-SG').id, required=True)
    district_id = fields.Many2one(
        'crm.district', 'Quận/Huyện', domain="[('state_id','=?',state_id),('country_id','=',country_id)]", track_visibility='always', required=True)
    type_of_road = fields.Selection(
        string='Loại đường', selection=TYPE_OF_ROAD, required=True, track_visibility='always')
    horizontal = fields.Float('Ngang', digits=dp.get_precision(
        'Product Unit of Measure'), track_visibility='always')
    # horizontal_uom = fields.Many2one('uom.uom','Unit of measure', default=lambda self: self.env.ref('uom.product_uom_meter'))
    length = fields.Float('Dài', digits=dp.get_precision(
        'Product Unit of Measure'), track_visibility='always')
    # length_uom = fields.Many2one('uom.uom','Unit of measure', default=lambda self: self.env.ref('uom.product_uom_meter'))
    back_expand = fields.Float('Nở hậu', digits=dp.get_precision(
        'Product Unit of Measure'), track_visibility='always')
    # back_expand_uom = fields.Many2one('uom.uom','Unit of measure', default=lambda self: self.env.ref('uom.product_uom_meter'))
    number_of_floors = fields.Float('Số tầng', digits=dp.get_precision(
        'Product Unit of Measure'), track_visibility='always')
    price = fields.Float('Giá', digits=dp.get_precision(
        'Product Price'), track_visibility='always')
    currency = fields.Selection(string='Tiền tệ',selection=[('usd','$'),('mil','Triệu'),('bil','Tỷ')])
    supporter_with_rule_ids = fields.One2many(comodel_name='crm.product.request.rule', inverse_name="crm_product_id", string='CV chăm sóc và phân quyền', track_visibility='always',
                                              domain=[('state', '=', 'approved')], ondelete='cascade',
                                              readonly=True, force_save=True)
    supporter_full_ids = fields.One2many(comodel_name='crm.product.request.rule', inverse_name="crm_product_id", string='Phân quyền',
                                         groups='bds.crm_product_change_rule_user,bds.crm_product_manager', ondelete='cascade')

    is_show_map_to_user = fields.Boolean(
        'Hiển Thị bản đồ cho KH', default=False)
    is_show_map = fields.Boolean('Xem bản đồ', compute="_compute_show_data")


    #Field for description
    location = fields.Char('Vị trí',)
    current_status = fields.Char('Hiện trạng',)
    convenient = fields.Char('Thuận tiện',)
    business_restrictions = fields.Char('Hạn chế kinh doanh',)
    rental_price = fields.Char('Giá cho thuê')
    note = fields.Text('Ghi chú')
    tip = fields.Float('Hoa hồng')
    source = fields.Char('Nguồn')
    way = fields.Char('Lối đi')
    adv = fields.Char('Quảng cáo')
    potential_evaluation = fields.Char('Đánh giá tiềm năng')

    
    @api.depends('rental_price','note','tip','potential_evaluation','source','adv','location','current_status','convenient','business_restrictions','requirement','type_of_real_estate','type_of_road','street','ward_no','district_id','horizontal','length','direction','way')
    def _set_description(self):
        description = '{nhucau} {loaibds} {loaiduong} - Đường {tenduong} - Phường {phuong} - Quận {quan}. \
                    DT: {ngang} x {dai}. Hướng nhà:{huongnha}. Lối đi: {loidi}.Vị trí: {vitri}. \
                        Hiện trạng: {hientrang}. Thuận tiện: {thuantien}. Hạn chế kinh doanh: {hckd}. \
                            Giá cho thuê: {giachothue}(thương lượng). Ghi chú: {ghichu}. Nguồn: {nguon}. \
                                Chủ nhà treo bảng QC: {treoquangcao}. Đánh giá sản phẩm: {danhgia}. Hoa hồng: {hoahong}'
        description = description.format(nhucau=self.requirement, loaibds=self.type_of_real_estate, loaiduong=self.type_of_road, tenduong=self.street.name, \
            phuong=self.ward_no.name, quan=self.district_id.name, ngang=self.horizontal, dai=self.length,huongnha=self.direction,\
                loidi=self.way,vitri=self.location,hientrang=self.current_status,thuantien=self.convenient,hckd=self.business_restrictions,\
                    giachothue=self.rental_price,ghichu=self.note,nguon=self.source,treoquangcao=self.adv,danhgia=self.potential_evaluation,hoahong=self.tip)
        return description
        

    @api.constrains('house_no', 'street')
    def _validate_house_no_street(self):
        for rec in self:
            if rec.house_no and rec.street.id:
                count = self.search_count([
                    ('house_no', '=', rec.house_no),
                    ('street', '=', rec.street.id),
                    ('id', '!=', rec.id)
                ])
                if count != 0:
                    raise exceptions.ValidationError('Số nhà: {}, đường {}, quận {} đã tồn tại'.format(
                        rec.house_no, rec.street.name, rec.street.district_id.name))

    @api.depends('supporter_with_rule_ids')
    def _compute_show_data(self):
        current_user = self.env.user
        for rec in self:
            rec.is_brokerage_specialist = False
            if current_user.has_group('bds.crm_product_manager') \
                    or current_user.has_group('bds.crm_product_rental_manager') or current_user.has_group('bds.crm_product_sale_manager'):
                rec.is_brokerage_specialist = True
            elif rec.brokerage_specialist.user_id == current_user \
                or current_user.has_group('bds.crm_product_rental_user_view_all')\
                     or current_user.has_group('bds.crm_product_sale_user_view_all'):
                rec.is_show_attachment = True
                rec.is_show_house_no = True
                rec.is_show_map = True
            else:
                employee_id = rec.supporter_with_rule_ids.filtered(
                    lambda r: r.employee_id.user_id == current_user and r.state == 'approved')
                rec.is_show_attachment = employee_id.is_show_attachment
                rec.is_show_house_no = employee_id.is_show_house_no
                rec.is_show_map = employee_id.is_show_map

    @api.depends('supporter_with_rule_ids')
    def _get_suppoter_ids(self):
        for rec in self:
            rec.supporter_ids = rec.supporter_with_rule_ids.mapped(
                'employee_id')

    @api.onchange('district_id')
    def _onchange_district(self):
        self.ensure_one()
        if self.district_id.id:
            self.state_id = self.district_id.state_id

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') != '':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'crm.product') or '/'
            vals['sequence'] = int(vals['name'][2:])
        res = super().create(vals)
        description = res._set_description()
        res['description'] = description
        return res

    @api.depends('name')
    def _is_manager(self):
        current_user = self.env.user
        for rec in self:
            is_manager = False
            if current_user.has_group('bds.crm_product_manager') \
            or current_user.has_group('bds.crm_product_rental_manager') or current_user.has_group('bds.crm_product_sale_manager'):
                is_manager = True
            print('is_manager: ',is_manager)
            rec.is_manager = is_manager          

    @api.multi
    def btn_request_rule(self):
        self.ensure_one()
        view_id = self.env.ref(
            'bds.crm_product_request_rule_sheet_view_form_wizard').id
        return {
            'name': 'Xin phân quyền',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'res_model': 'crm.product.request.rule.sheet',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': False,
        }
