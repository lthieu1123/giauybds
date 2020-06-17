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
    customer_uid = fields.Char(string='Mã KH', required=True,track_visibility='always')
    email = fields.Char('Email')
    financial_capability = fields.Char('Khả năng tài chính',track_visibility='always')
    zone = fields.Char('Khu vực hoạt động', track_visibility='always')
    
    is_show_email = fields.Boolean('Show Email', compute='_compute_show_data')
    supporter_with_rule_ids = fields.One2many(comodel_name='crm.request.request.rule', inverse_name="crm_product_id", string='CV chăm sóc và phân quyền', track_visibility='always',
                                              domain=[('state', '=', 'approved')], ondelete='cascade',
                                              readonly=True, force_save=True)
    supporter_full_ids = fields.One2many(comodel_name='crm.request.request.rule', inverse_name="crm_product_id", string='Phân quyền',
                                         groups='bds.crm_request_change_rule_user,bds.crm_request_manager', ondelete='cascade')


    @api.depends('supporter_with_rule_ids')
    def _compute_show_data(self):
        current_user = self.env.user
        for rec in self:
            rec.is_brokerage_specialist = False
            if rec.brokerage_specialist.user_id == current_user \
                or current_user.has_group('bds.crm_request_manager') \
                    or current_user.has_group('bds.crm_request_rental_manager') or current_user.has_group('bds.crm_request_sale_manager'):
                rec.is_brokerage_specialist = True
            employee_id = rec.supporter_with_rule_ids.filtered(
                lambda r: r.employee_id.user_id == current_user and r.state == 'approved')
            rec.is_show_attachment = employee_id.is_show_attachment
            rec.is_show_email = employee_id.is_show_email
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
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