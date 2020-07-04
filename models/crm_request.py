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
    requirement = fields.Selection(string='Nhu cầu', selection=REQUIREMENT_REQUEST, track_visibility='always')
    email = fields.Char('Email')
    financial_capability = fields.Float('Khả năng tài chính', digits=dp.get_precision(
        'Product Price'), track_visibility='always')
    currency = fields.Selection(string='Tiền tệ',selection=[('usd','$'),('mil','Triệu'),('bil','Tỷ')])
    zone = fields.Char('Khu vực hoạt động', track_visibility='always')
    business_demand = fields.Selection(string='Nhu cầu KD',selection=NCKD)
    
    is_show_email = fields.Boolean('Show Email', compute='_compute_show_data')
    supporter_with_rule_ids = fields.One2many(comodel_name='crm.request.request.rule', inverse_name="crm_product_id", string='CV chăm sóc và phân quyền', track_visibility='always',
                                              domain=[('state', '=', 'approved')], ondelete='cascade')
    supporter_full_ids = fields.One2many(comodel_name='crm.request.request.rule', inverse_name="crm_product_id", string='Phân quyền',
                                         groups='bds.crm_request_manager', ondelete='cascade')
    

    #Field for description
    way = fields.Char('Tập trung tuyến đường')
    dientich = fields.Char('Diện tích dao động')
    min_horizontal = fields.Char('Ngang tối thiểu')
    parking_lot = fields.Char('Chỗ để xe')
    partner_kd = fields.Char('Chủ KD hiện tại')
    note = fields.Text('Ghi chú')
    source = fields.Char('Nguồn')
    potential_evaluation = fields.Char('Đánh giá tiềm năng')

    #Search fields
    phone_number_search = fields.Char(compute='_do_something_search',search='_search_phone_number',string='Số ĐT')

    def _do_something_search(self):
        pass
    
    def _get_fields_to_ignore_in_search(self):
        return ['host_number_1','host_number_2','host_number_3',]

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
        if current_user.has_group('bds.crm_request_manager'):
            return []
    
        if (current_user.has_group('bds.crm_request_rental_manager') or current_user.has_group('bds.crm_request_rental_user_view_all')) or (current_user.has_group('bds.crm_request_sale_user_view_all') or current_user.has_group('bds.crm_request_sale_manager')):
            if (current_user.has_group('bds.crm_request_rental_manager') or current_user.has_group('bds.crm_request_rental_user_view_all')) and (current_user.has_group('bds.crm_request_sale_user_view_all') or current_user.has_group('bds.crm_request_sale_manager')):
                domain  = ['|',('requirement','=','rental'),('requirement','=','sale')]
            elif current_user.has_group('bds.crm_request_rental_manager') or current_user.has_group('bds.crm_request_rental_user_view_all'):
                domain  = [('requirement','=','rental')]
            else:
                domain  = [('requirement','=','sale')]    
        else:
            if current_user.has_group('bds.crm_request_rental_user') and current_user.has_group('bds.crm_request_sale_user'):
                domain =  ['|',('requirement','=','rental'),('requirement','=','sale'),'|',('brokerage_specialist','=',employee_id),('supporter_ids','=',employee_id)] + domain
            elif current_user.has_group('bds.crm_request_rental_user'):
                domain =  [('requirement','=','rental'),'|',('brokerage_specialist','=',employee_id),('supporter_ids','=',employee_id)]
            else:
                domain =  [('requirement','=','sale'),'|',('brokerage_specialist','=',employee_id),('supporter_ids','=',employee_id)]
        return domain

    @api.multi
    def _search_phone_number(self, operator, value):
        main_domain = ['|','|',('host_number_1','=',value),('host_number_2','=',value),('host_number_3','=',value)]
        domain = self._get_domain_default()
        return domain + main_domain
    


    @api.depends('financial_capability','currency','partner_kd','potential_evaluation','note','source','type_of_real_estate','type_of_road','zone','business_demand','way','dientich','min_horizontal','parking_lot')
    def _set_description(self):
        for rec in self:
            description = 'Khách hàng {nhucau} {loaibds}  - {loaiduong} - {khuvuc}, nhu cầu kinh doanh: {nckd}. Tập trung tuyến đường {way}. Tài chính dao động: {gia}.Cần diện tích dao động: {dientich} - Ngang tối thiểu: {min}, Cần chỗ để xe khoảng: {dexe}. Hiện đang là chủ kinh doanh: {ckd}. Đánh giá mức độ tiềm năng: {danhgia}. Ghi chú: {note}. Nguồn: {nguon}'
             #Get value from selection fields
            requirement = dict(REQUIREMENT_REQUEST)
            nhucau = requirement.get(rec.requirement,'')
            type_of_real_estate = dict(TYPE_OF_REAL_ESTATE)
            loaibds=type_of_real_estate.get(rec.type_of_real_estate,'')
            type_of_road = dict(TYPE_OF_ROAD)
            loaiduong = type_of_road.get(rec.type_of_road,'')
            business_demand = dict(NCKD)
            nckd = business_demand.get(rec.business_demand,'')
            gia = '%s %s' % (rec.financial_capability,rec.currency)

            description = description.format(nhucau=nhucau,loaibds=loaibds, loaiduong=loaiduong, khuvuc=rec.zone,nckd=nckd,\
                way=rec.way,gia=gia,dientich=rec.dientich, min=rec.min_horizontal, dexe=rec.parking_lot,\
                    ckd=rec.partner_kd,danhgia=rec.potential_evaluation,note=rec.note,nguon=rec.source)
            rec.description = description

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


    @api.depends('supporter_with_rule_ids','supporter_with_rule_ids.state')
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
            vals['sequence'] = int(vals['name'][2:])
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

    @api.model
    def _adjust_price(self):
        # self.env.cr.execute("update crm_request set price = price / 1000 where price > 999.99")
        sub_query = """
            select tmp.{}
                from (select
                    id as id,
                    name as name,
                    row_number() OVER () as count,
                    case
                        when row_number() OVER () < 10 then right(concat('KH00000',row_number() OVER ()),8 )
                        when row_number() OVER () > 9 and row_number() OVER () < 100 then right(concat('KH0000',row_number() OVER ()),8 )
                        when row_number() OVER () > 99 and row_number() OVER () < 1000 then right(concat('KH000',row_number() OVER ()),8 )
                        when row_number() OVER () > 999 and row_number() OVER () < 10000 then right(concat('KH00',row_number() OVER ()),8 )
                        when row_number() OVER () > 9999 and row_number() OVER () < 100000 then right(concat('KH0',row_number() OVER ()),8 )
                    end as name_new
                from crm_request) as tmp
                where tmp.id = crm_request.id 
        """
        name = sub_query.format('name_new')
        count = sub_query.format('count')
        self.env.cr.execute("""
            update crm_request
            set name = ({}),
            sequence = ({})
            """.format(name,count))