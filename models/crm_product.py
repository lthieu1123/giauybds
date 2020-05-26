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



class CrmProduct(models.Model):
    _name = 'crm.product'
    _description = 'CRM Product'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def _default_stage(self):
        return self.env['crm.states.product'].search([], limit=1, order='sequence').id

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        return self.env['crm.states.product'].search([])

    states = fields.Many2one('crm.states.product', string='Trạng thái', default=_default_stage,
                            track_visibility='always', group_expand='_read_group_stage_ids', store=True)

    sequence = fields.Integer(string='Số TT', readonly=True, force_save=True)
    name = fields.Char(string='Số đăng ký', default='New', readonly=True, force_save=True)
    requirement = fields.Selection(string='Nhu cầu', selection=[('rental','Cho thuê'),('sale','Cần bán')])
    type_of_real_estate = fields.Selection(string='Loại BĐS', selection=TYPE_OF_REAL_ESTATE, required=True)
    
    #Address
    house_no = fields.Char('Số nhà')
    ward_no = fields.Char('Phường/Xã')
    street = fields.Char('Đường')
    country_id = fields.Many2one('res.country', 'Quốc gia', default= lambda self: self.env.ref('base.vn'))
    state_id = fields.Many2one('res.country.state','Tỉnh/TP', domain = "[('country_id','=',country_id)]")
    district_id = fields.Many2one('crm.district', 'Quận/Huyện', domain = "[('state_id','=?',state_id),('country_id','=',country_id)]")
    type_of_road = fields.Selection(string='Loại đường', selection=TYPE_OF_ROAD,required=True)
    horizontal = fields.Float('Ngang', digits=dp.get_precision('Product Unit of Measure'))
    # horizontal_uom = fields.Many2one('uom.uom','Unit of measure', default=lambda self: self.env.ref('uom.product_uom_meter'))
    length = fields.Float('Dài', digits=dp.get_precision('Product Unit of Measure'))
    # length_uom = fields.Many2one('uom.uom','Unit of measure', default=lambda self: self.env.ref('uom.product_uom_meter'))
    back_expand = fields.Float('Nở hậu',digits=dp.get_precision('Product Unit of Measure'))
    # back_expand_uom = fields.Many2one('uom.uom','Unit of measure', default=lambda self: self.env.ref('uom.product_uom_meter'))
    number_of_floors = fields.Float('Số tầng',digits=dp.get_precision('Product Unit of Measure'))
    usd_price = fields.Float('Giá USD', digits=dp.get_precision('Product Price'))
    vnd_price = fields.Float('Giá VND', digits=dp.get_precision('Product Price'))
    brokerage_specialist = fields.Many2one('res.users','CV môi giới', default=lambda self: self.env.user)
    supporter = fields.Many2one('res.users','CV chăm sóc')
    direction = fields.Selection(string='Hướng',selection=CARDINAL_DIRECTION,)
    description = fields.Text('Diễn giải')
    host_name = fields.Char('Tên chủ')
    host_number_1 = fields.Char('Số ĐT 1')
    host_number_2 = fields.Char('Số ĐT 2')
    host_number_3 = fields.Char('Số ĐT 3')
    is_show_map = fields.Boolean('Hiển thị trên bản đồ', default=False)
    is_show_house_no = fields.Boolean('Hiển thị số nhà',compute='_is_show_house_no')


    @api.onchange('district_id')
    def _onchange_district(self):
        self.ensure_one()
        if self.district_id.id:
            self.state_id = self.district_id.state_id

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('crm.product') or '/'
            vals['sequence'] = int(vals['name'].split('-')[1])
        res = super().create(vals)
        return res
    
    @api.depends('name')
    def _is_show_house_no(self):
        for rec in self:
            rec.is_show_house_no = True if rec.brokerage_specialist == self.env.user else False

