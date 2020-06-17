# -*- coding: utf-8 -*-

import json
import logging

from odoo import _, api, fields, models, registry, exceptions
from odoo.exceptions import UserError
from odoo.tools.translate import _
from odoo.addons import decimal_precision as dp
from ..commons.bds_constant import *
from datetime import datetime


class CrmProductReuqestRule(models.Model):
    _name = 'crm.product.request.rule'
    _description = 'CRM Product Request Rule'
    _inherit = 'crm.request.rule.abstract.model'
    
    crm_product_id = fields.Many2one('crm.product','CRM Product',ondelete='cascade')
    crm_request_sheet_id = fields.Many2one('crm.product.request.rule.sheet','Sheet')
    is_show_attachment = fields.Boolean('Xem hình ảnh', default=False)
    is_show_house_no = fields.Boolean('Xem số nhà', default=False)
    is_show_map = fields.Boolean('Xem bản đồ', default=False)
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('crm.product.request.rule') or '/'
            vals['sequence'] = int(vals['name'].split('-')[1])
        res = super().create(vals)
        return res

class CrmProductReuqestRuleSheet(models.Model):
    _name = 'crm.product.request.rule.sheet'
    _description = 'CRM Product Request Rule Sheet'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Tên', default='New', readonly=True, force_save=True, track_visibility='always')
    employee_id = fields.Many2one('hr.employee','CV chăm sóc',ondelete='cascade', default= lambda self: self._get_default_employee_id())
    crm_request_line_ids = fields.One2many(comodel_name='crm.product.request.rule',inverse_name="crm_request_sheet_id",string='CV chăm sóc')
    state = fields.Selection(string='Trạng thái', selection=[('draft','Chưa duyệt'),('approved','Đã duyệt'),('cancel','Từ chối')], default="draft")
    requirement = fields.Selection(string='Nhu cầu', selection=[('rental','Cho thuê'),('sale','Cần bán')], compute='_set_requirement')

    @api.depends('crm_request_line_ids')
    def _set_requirement(self):
        for rec in self:
            sale_count = len(rec.crm_request_line_ids.filtered(lambda r: r.requirement == 'sale').ids)
            rental_count = len(rec.crm_request_line_ids.filtered(lambda r: r.requirement == 'rental').ids)
            if sale_count and rental_count:
                raise exceptions.VallidationError('Không thể chọn 2 yêu cầu cho thuê và bán trong cùng 1 bảng xin phân quyền.')
            elif sale_count and rental_count==0:
                rec.requirement = 'sale'
            else:
                rec.requirement = 'rental'
    

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
                crm_request_line_value = self._prepare_crm_request_line(self.env['crm.product'].browse(_id))
                product_lines.append((0, 0, crm_request_line_value))
            self.crm_request_line_ids = product_lines


    def _prepare_crm_request_line(self,crm_product_id):
        return {
            'employee_id': self.employee_id.id,
            'crm_product_id': crm_product_id.id,
            'requirement': crm_product_id.requirement,
        }
    
    def send_notification_request(self):
        requirement = self.requirement
        groups_id = []
        if requirement == 'sale':
            groups_id.append(self.env.ref('bds.crm_product_change_rule_user').id)
            groups_id.append(self.env.ref('bds.crm_product_sale_manager').id)
            groups_id.append(self.env.ref('bds.crm_product_manager').id)
        else:
            groups_id.append(self.env.ref('bds.crm_product_change_rule_user').id)
            groups_id.append(self.env.ref('bds.crm_product_rental_manager').id)
            groups_id.append(self.env.ref('bds.crm_product_manager').id)
        user_ids = self.env['res.users'].search([
            ('groups_id','in',groups_id)
        ])
        for user in user_ids:
            mess = BODY_MSG.format(user.partner_id.id,user.partner_id.id,user.partner_id.name,"Vui lòng duyệt yêu cầu")
            self.message_post(body=mess,message_type="comment")

    def send_notification_approve(self):
        user = self.employee_id.user_id
        mess = BODY_MSG.format(user.partner_id.id,user.partner_id.id,user.partner_id.name,"Đã duyệt")
        self.message_post(body=mess)

    @api.multi
    def btn_save(self):
        self.send_notification_request()
        context = self.env.context.copy()
        context['default_message'] = 'Yêu cầu phân quyền đã được gửi. Vui lòng chờ phản hồi từ cấp cao hơn'
        return {
            'name': 'Xin phân quyền',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'announce',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
            'res_id': False,
        }

    @api.multi
    def btn_approve(self):
        self.ensure_one()
        self.update({
            'state': 'approved'
        })
        request_rule = self.env['crm.product.request.rule']
        for line in self.crm_request_line_ids:
            existed_line_id = request_rule.search([
                ('employee_id','=',line.employee_id.id),
                ('crm_product_id','=',line.crm_product_id.id),
                ('state','=','approved')
            ])
            if existed_line_id.id:
                existed_line_id.write({
                    'state':'closed',
                })
            line.write({
                'state':'approved',
                'approved_date': datetime.now(),
                'approver': self.env.user.employee_ids.ids[0]
            })
        self.send_notification_approve()
               

    @api.multi
    def btn_reject(self):
        self.crm_request_line_ids.write({
            'state':'cancel',
            'approved_date': datetime.now(),
            'approver': self.env.user.employee_ids.ids[0]
        })

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('crm.product.request.rule.sheet') or '/'
            vals['sequence'] = int(vals['name'].split('-')[1])
        res = super().create(vals)
        return res