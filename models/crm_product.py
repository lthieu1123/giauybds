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
    currency = fields.Selection(string='Tiền tệ',selection=CURRENCY)
    supporter_with_rule_ids = fields.One2many(comodel_name='crm.product.request.rule', inverse_name="crm_product_id", string='CV chăm sóc và phân quyền', track_visibility='always',
                                              domain=[('state', '=', 'approved')], ondelete='cascade')
    supporter_full_ids = fields.One2many(comodel_name='crm.product.request.rule', inverse_name="crm_product_id", string='Phân quyền',
                                         groups='bds.crm_product_manager', ondelete='cascade')

    is_show_map_to_user = fields.Boolean(
        'Hiển Thị bản đồ cho KH', default=False)
    is_show_map = fields.Boolean('Xem bản đồ', compute="_compute_show_data")
    is_duplicate_house_no = fields.Boolean('Trùng số nhà',)


    #Field for description
    location = fields.Char('Vị trí',)
    current_status = fields.Char('Hiện trạng',)
    convenient = fields.Char('Thuận tiện',)
    business_restrictions = fields.Char('Hạn chế kinh doanh',)
    note = fields.Text('Ghi chú')
    tip = fields.Char('Hoa hồng')
    source = fields.Char('Nguồn')
    way = fields.Char('Lối đi')
    adv = fields.Char('Quảng cáo')
    potential_evaluation = fields.Char('Đánh giá tiềm năng')

    #Search fields
    phone_number_search = fields.Char(compute='_do_something_search',search='_search_phone_number',string='Số ĐT')
    house_no_search = fields.Char(compute='_do_something_search', search='_search_house_no', string='Số nhà')


    def _do_something_search(self):
        pass
    
    def _get_fields_to_ignore_in_search(self):
        return ['host_number_1','host_number_2','host_number_3','house_no']

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        res = super().fields_get(allfields, attributes=attributes)
        for field in self._get_fields_to_ignore_in_search():
            if res.get(field):
                res.get(field)['searchable'] = False
        return res

    def _get_domain_default(self):
        current_user = self.env.user
        employee_id = current_user.employee_ids.ids[0]
        if current_user.has_group('bds.crm_product_manager'):
            return []
    
        if (current_user.has_group('bds.crm_product_rental_manager') or current_user.has_group('bds.crm_product_rental_user_view_all')) or (current_user.has_group('bds.crm_product_sale_user_view_all') or current_user.has_group('bds.crm_product_sale_manager')):
            if (current_user.has_group('bds.crm_product_rental_manager') or current_user.has_group('bds.crm_product_rental_user_view_all')) and (current_user.has_group('bds.crm_product_sale_user_view_all') or current_user.has_group('bds.crm_product_sale_manager')):
                domain  = ['|',('requirement','=','rental'),('requirement','=','sale')]
            elif current_user.has_group('bds.crm_product_rental_manager') or current_user.has_group('bds.crm_product_rental_user_view_all'):
                domain  = [('requirement','=','rental')]
            else:
                domain  = [('requirement','=','sale')]    
        else:
            if current_user.has_group('bds.crm_product_rental_user') and current_user.has_group('bds.crm_product_sale_user'):
                domain =  ['|',('requirement','=','rental'),('requirement','=','sale'),'|',('brokerage_specialist','=',employee_id),('supporter_ids','=',employee_id)] + domain
            elif current_user.has_group('bds.crm_product_rental_user'):
                domain =  [('requirement','=','rental'),'|',('brokerage_specialist','=',employee_id),('supporter_ids','=',employee_id)]
            else:
                domain =  [('requirement','=','sale'),'|',('brokerage_specialist','=',employee_id),('supporter_ids','=',employee_id)]
        return domain

    @api.multi
    def _search_phone_number(self, operator, value):
        main_domain = ['|','|',('host_number_1','ilike',value),('host_number_2','ilike',value),('host_number_3','ilike',value)]
        domain = self._get_domain_default()
        return domain + main_domain
    
    @api.multi
    def _search_house_no(self, operator, value):
        main_domain = [('house_no','ilike',value)]
        domain = self._get_domain_default()
        return domain + main_domain
    
    @api.depends('price','currency','note','tip','potential_evaluation','source','adv','location','current_status','convenient','business_restrictions','requirement','type_of_real_estate','type_of_road','street','ward_no','district_id','horizontal','length','direction','way')
    def _set_description(self):
        for rec in self:
            description = '{nhucau} {loaibds} {loaiduong} - Đường {tenduong} - Phường {phuong} - Quận {quan}. DT: {ngang} x {dai}. Hướng nhà:{huongnha}. Lối đi: {loidi}.Vị trí: {vitri}. Hiện trạng: {hientrang}. Thuận tiện: {thuantien}. Hạn chế kinh doanh: {hckd}. Giá: {giachothue}(thương lượng). Ghi chú: {ghichu}. Nguồn: {nguon}. Chủ nhà treo bảng QC: {treoquangcao}. Đánh giá sản phẩm: {danhgia}. Hoa hồng: {hoahong}'
            #Get value from selection fields
            requirement = dict(REQUIREMENT_PRODUCT)
            nhucau = requirement.get(rec.requirement,'')
            type_of_real_estate = dict(TYPE_OF_REAL_ESTATE)
            loaibds=type_of_real_estate.get(rec.type_of_real_estate,'')
            type_of_road = dict(TYPE_OF_ROAD)
            loaiduong = type_of_road.get(rec.type_of_road,'')
            direction = dict(CARDINAL_DIRECTION)
            huongnha = direction.get(rec.direction,'')
            currency = dict(CURRENCY)
            giachothue = '%s %s' % (rec.price,currency.get(rec.currency,''))

            description = description.format(nhucau=nhucau, loaibds=loaibds, loaiduong=loaiduong, tenduong=rec.street.name, \
                phuong=rec.ward_no.name, quan=rec.district_id.name, ngang=rec.horizontal, dai=rec.length,huongnha=huongnha,\
                    loidi=rec.way,vitri=rec.location,hientrang=rec.current_status,thuantien=rec.convenient,hckd=rec.business_restrictions,\
                        giachothue=giachothue,ghichu=rec.note,nguon=rec.source,treoquangcao=rec.adv,danhgia=rec.potential_evaluation,hoahong=rec.tip)
            rec.description = description
    
    @api.onchange('house_no', 'street')
    def _check_house_no(self):
        print('_check_house_no')
        is_duplicate_house_no = False            
        if self.house_no and self.street.id:
            if self.house_no != self._origin.house_no or self.street.id != self._origin.street.id:
                count = self.search_count([
                    ('house_no', '=', self.house_no),
                    ('street', '=', self.street.id),
                    ('id','!=',self._origin.id)
                ])
                is_duplicate_house_no = True if count >= 1 else False
        self.is_duplicate_house_no = is_duplicate_house_no

            

    @api.constrains('house_no', 'street')
    def _validate_house_no_street(self):
        for rec in self:
            count = self.search_count([
                ('house_no', '=', self.house_no),
                ('street', '=', self.street.id),
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

    @api.depends('supporter_with_rule_ids','supporter_with_rule_ids.state')
    def _get_suppoter_ids(self):
        for rec in self:
            rec.supporter_ids = rec.supporter_with_rule_ids.filtered(lambda r: r.state=='approved').mapped('employee_id')

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
        return res

    @api.depends('name')
    def _is_manager(self):
        current_user = self.env.user
        for rec in self:
            is_manager = False
            if current_user.has_group('bds.crm_product_manager') \
            or current_user.has_group('bds.crm_product_rental_manager') or current_user.has_group('bds.crm_product_sale_manager'):
                is_manager = True
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
    
    @api.model
    def _adjust_price(self):
        self.env.cr.execute("update crm_product set price = price / 1000 where price > 999.99")
        sub_query = """
            select tmp.{}
                from (select
                    id as id,
                    name as name,
                    row_number() OVER () as count,
                    case
                        when row_number() OVER () < 10 then right(concat('SP00000',row_number() OVER ()),8 )
                        when row_number() OVER () > 9 and row_number() OVER () < 100 then right(concat('SP0000',row_number() OVER ()),8 )
                        when row_number() OVER () > 99 and row_number() OVER () < 1000 then right(concat('SP000',row_number() OVER ()),8 )
                        when row_number() OVER () > 999 and row_number() OVER () < 10000 then right(concat('SP00',row_number() OVER ()),8 )
                        when row_number() OVER () > 9999 and row_number() OVER () < 100000 then right(concat('SP0',row_number() OVER ()),8 )
                    end as name_new
                from crm_product) as tmp
                where tmp.id = crm_product.id 
        """
        name = sub_query.format('name_new')
        count = sub_query.format('count')
        self.env.cr.execute("""
            update crm_product
            set name = ({}),
            sequence = ({})
            """.format(name,count))
