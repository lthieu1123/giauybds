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
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'customer_uid'


    @api.model
    def _default_stage(self):
        return self.env['crm.states.request'].search([], limit=1, order='sequence').id

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        return self.env['crm.states.request'].search([])

    state = fields.Many2one('crm.states.request', string='State', default=_default_stage,
                            track_visibility='always', group_expand='_read_group_stage_ids', store=True)

    sequence = fields.Integer(string='Sequence')
    customer_uid = fields.Char(string='Customer id', required=True)
    customer_name = fields.Char(string='Customer name')
    request = fields.Selection(string='Request', selection=[('rent','Need to rent'),('buy','Need to buy')])
    customer_number_1 = fields.Char('Phone number 1')
    customer_number_2 = fields.Char('Phone number 2')
    customer_number_3 = fields.Char('Phone number 3')
    email = fields.Char('Email')
    financial_capability = fields.Char('Financial capability')
    zone = fields.Char('Zone')
    brokerage_specialist = fields.Many2one('res.users','Brokerage specialist', default=lambda self: self.env.user)
    supporter = fields.Many2one('res.users','Supporter')
    type_of_real_estate = fields.Selection(string='Types of Real Estate', selection=TYPE_OF_REAL_ESTATE, required=True)
    direction = fields.Selection(string='Direction',selection=[('w_www','Tây-TTT'),('wn_www','Tây Nam - TTT')])
    description = fields.Text('Description')