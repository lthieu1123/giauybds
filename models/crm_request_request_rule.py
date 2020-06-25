import json
import logging

from odoo import _, api, fields, models, registry, exceptions
from odoo.exceptions import UserError
from odoo.tools.translate import _
from odoo.addons import decimal_precision as dp
from ..commons.bds_constant import *
from datetime import datetime


class CrmReuqestReuqestRule(models.Model):
    _name = 'crm.request.request.rule'
    _description = 'CRM Request Request Rule'
    _inherit = 'crm.product.request.rule'


    crm_product_id = fields.Many2one('crm.request','CRM Product',ondelete='cascade')
    crm_request_sheet_id = fields.Many2one('crm.request.request.rule.sheet','Sheet')
    is_show_attachment = fields.Boolean('Xem hình ảnh', default=True)
    is_show_house_no = fields.Boolean('Xem số nhà', default=True)
    is_show_email = fields.Boolean('Xem Email', default=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('crm.request.request.rule') or '/'
            vals['sequence'] = int(vals['name'].split('-')[1])
        res = super().create(vals)
        return res

class CrmRequestRequestRuleSheet(models.Model):
    _name = 'crm.request.request.rule.sheet'
    _description = 'CRM Request Request Rule Sheet'
    _inherit = 'crm.product.request.rule.sheet'

    crm_request_line_ids = fields.One2many(comodel_name='crm.request.request.rule',inverse_name="crm_request_sheet_id",string='CV chăm sóc')

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        context = self.env.context.copy()
        if context.get('active_ids',False) and context.get('active_model','') == 'crm.request':
            product_lines = []
            ids = context.get('active_ids')
            for _id in ids:
                crm_request_line_value = self._prepare_crm_request_line(self.env['crm.request'].browse(_id))
                product_lines.append((0, 0, crm_request_line_value))
            self.crm_request_line_ids = product_lines

    def send_notification_request(self):
        requirement = self.requirement
        groups_id = []
        if requirement == 'sale':
            groups_id.append(self.env.ref('bds.crm_request_change_rule_user').id)
            groups_id.append(self.env.ref('bds.crm_request_sale_manager').id)
            groups_id.append(self.env.ref('bds.crm_request_manager').id)
        else:
            groups_id.append(self.env.ref('bds.crm_request_change_rule_user').id)
            groups_id.append(self.env.ref('bds.crm_request_rental_manager').id)
            groups_id.append(self.env.ref('bds.crm_request_manager').id)
        user_ids = self.env['res.users'].search([
            ('groups_id','in',groups_id)
        ])
        for user in user_ids:
            mess = BODY_MSG.format(user.partner_id.id,user.partner_id.id,user.partner_id.name,"Vui lòng duyệt yêu cầu")
            self.message_post(body=mess,message_type="comment")

    @api.multi
    def btn_approve(self):
        self.ensure_one()
        self.update({
            'state': 'approved'
        })
        request_rule = self.env['crm.request.request.rule']
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
               

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('crm.request.request.rule.sheet') or '/'
            vals['sequence'] = int(vals['name'].split('-')[1])
        res = super().create(vals)
        return res