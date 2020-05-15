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

    states = fields.Many2one('crm.states.product', string='State', default=_default_stage,
                            track_visibility='always', group_expand='_read_group_stage_ids', store=True)

    sequence = fields.Integer(string='Sequence')
    name = fields.Char(string='Register No')
    requirement = fields.Selection(string='Requirement', selection=[('rental','Rental'),('sale','Sale')])
    type_of_real_estate = fields.Selection(string='Types of Real Estate', selection=TYPE_OF_REAL_ESTATE, required=True)
    
    #Address
    house_no = fields.Char('House No')
    ward_no = fields.Char('Ward')
    street = fields.Char('Street')
    state = fields.Many2one('res.country.state','State')
    city = fields.Many2one('crm.city', 'City',)
    country = fields.Many2one('res.country', 'Country', default= lambda self: self.env.ref('base.vn'))
    type_of_road = fields.Selection(string='Type of road', selection=TYPE_OF_ROAD,required=True)
    horizontal = fields.Float('Horizontal', digits=dp.get_precision('Product Unit of Measure'))
    horizontal_uom = fields.Many2one('uom.uom','Unit of measure', default=lambda self: self.env.ref('uom.product_uom_meter'))
    long = fields.Float('Long', digits=dp.get_precision('Product Unit of Measure'))
    long_uom = fields.Many2one('uom.uom','Unit of measure', default=lambda self: self.env.ref('uom.product_uom_meter'))
    back_expand = fields.Float('Back Expand',digits=dp.get_precision('Product Unit of Measure'))
    back_expand_uom = fields.Many2one('uom.uom','Unit of measure', default=lambda self: self.env.ref('uom.product_uom_meter'))
    number_of_floors = fields.Float('Number of Floors',digits=dp.get_precision('Product Unit of Measure'))
    usd_price = fields.Float('USD Price', digits=dp.get_precision('Product Price'))
    vnd_price = fields.Float('VND Price', digits=dp.get_precision('Product Price'))
    brokerage_specialist = fields.Many2one('res.users','Brokerage specialist', default=lambda self: self.env.user)
    supporter = fields.Many2one('res.users','Supporter')
    direction = fields.Selection(string='Direction',selection=[('w_www','Tây-TTT'),('wn_www','Tây Nam - TTT')])
    description = fields.Text('Description')
    host_name = fields.Char('Host name')
    host_number_1 = fields.Char('Phone number 1')
    host_number_2 = fields.Char('Phone number 2')
    host_number_3 = fields.Char('Phone number 3')
    register_date = fields.Date('Register Date', default=fields.Datetime.now)
    is_show_map = fields.Boolean('Is show map', defualt=False)
