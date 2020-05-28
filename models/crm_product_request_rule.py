# -*- coding: utf-8 -*-

import json
import logging

from odoo import _, api, fields, models, registry
from odoo.exceptions import UserError
from odoo.tools.translate import _
from odoo.addons import decimal_precision as dp
from ..commons.bds_constant import *
from datetime import datetime


class CrmProductReuqestRule(models.Model):
    _name = 'crm.product.request.rule'
    _description = 'CRM Product Request Rule'
    

    crm_product_id = fields.Many2one('crm.product','CRM Product',ondelete='cascade')
    employee_id = fields.Many2one('hr.employee','CV chăm sóc',ondelete='cascade')
    crm_request_sheet_id = fields.Many2one('crm.product.request.rule.sheet','Sheet')
    is_show_attachment = fields.Boolean('Xem hình ảnh', default=False)
    is_show_house_no = fields.Boolean('Xem số nhà', default=False)
    is_show_description = fields.Boolean('Xem diễn giải', default=False)
    is_show_phone_no = fields.Boolean('Xem số ĐT', default=False)
    is_show_map = fields.Boolean('Xem bản đồ', default=False)
    approver = fields.Many2one('hr.employee', 'Người duyệt')
    state = fields.Selection(string='Trạng thái', selection=[('draft','Chưa duyệt'),('approved','Đã duyệt'),('cancel','Từ chối')], default="draft")
    approved_date = fields.Datetime(string='Ngày duyệt')

class CrmProductReuqestRuleSheet(models.Model):
    _name = 'crm.product.request.rule.sheet'
    _description = 'CRM Product Request Rule Sheet'

    name = fields.Char('name')
    employee_id = fields.Many2one('hr.employee','CV chăm sóc',ondelete='cascade', default= lambda self: self._get_default_employee_id())
    crm_request_line_ids = fields.One2many(comodel_name='crm.product.request.rule',inverse_name="crm_request_sheet_id",string='CV chăm sóc')
    state = fields.Selection(string='Trạng thái', selection=[('draft','Chưa duyệt'),('approved','Đã duyệt'),('cancel','Từ chối')], default="draft")

    def _get_default_employee_id(self):
        return self.env['hr.employee'].search([
            ('user_id','=',self.env.user.id)
        ]).id

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        context = self.env.context.copy()
        if context.get('active_ids',False) and context.get('active_model','') == 'crm.product':
            product_lines = []
            ids = context.get('active_ids')
            for _id in ids:
                crm_request_line_value = self._prepare_crm_request_line(_id)
                product_lines.append((0, 0, crm_request_line_value))
            self.crm_request_line_ids = product_lines


    def _prepare_crm_request_line(self,_id):
        return {
            'employee_id': self.employee_id.id,
            'crm_product_id': _id
        }
    
    @api.multi
    def btn_save(self):
        context = self.env.context.copy()
        context['default_message'] = 'Yêu cầu phân quyền đã được gửi. Vui lòng chờ phản hồi từ cấp cao hơn'
        return {
            'name': 'Xin phân quyền',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'ecc.announce',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': False,
        }

    @api.multi
    def btn_approve(self):
        self.ensure_one()
        request_rule = self.env['crm.product.request.rule']
        for line in self.crm_request_line_ids:
            existed_line_id = request_rule.search([
                ('employee_id','=',line.employee_id.id),
                ('crm_product_id','=',line.crm_product_id.id),
                ('state','=','approved')
            ])
            if existed_line_id.id:
                existed_line_id.is_show_attachment = line.is_show_attachment
                existed_line_id.is_show_house_no = line.is_show_house_no
                existed_line_id.is_show_description = line.is_show_description
                existed_line_id.is_show_phone_no = line.is_show_phone_no
                existed_line_id.is_show_attachment = line.is_show_phone_no
                existed_line_id.approved_date = datetime.now()
            else:
                existed_line_id.write({
                    'state':'approved',
                    'approved_date': datetime.now()
                })

    @api.multi
    def btn_reject(self):
        self.ensure_one()
        self.crm_request_line_ids.write({
            'state':'approved',
            'approved_date': datetime.now()
        })
