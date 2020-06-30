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

    def get_default_product(self):
        return self.env.context.get('default_product',False)

    crm_product_id = fields.Many2one('crm.request','CRM Product',ondelete='cascade')
    crm_request_sheet_id = fields.Many2one('crm.request.request.rule.sheet','Sheet')
    is_show_attachment = fields.Boolean('Xem hình ảnh', default=True)
    is_show_house_no = fields.Boolean('Xem số nhà', default=True)
    is_show_email = fields.Boolean('Xem Email', default=True)
    requirement = fields.Selection(string='Nhu cầu', selection=[('rental','Cần thuê'),('sale','Cần mua')])

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('crm.request.request.rule') or '/'
            vals['sequence'] = int(vals['name'].split('-')[1])
        res = super().create(vals)
        return res

    @api.onchange('requirement')
    def _domain_employee(self):
        domain = []
        if self.requirement == 'sale':
            user_sale_group_id = self.env.ref('bds.crm_request_sale_user').id
            domain = [
                ('user_id.groups_id','=',user_sale_group_id)
            ]
        else:
            user_rental_group_id = self.env.ref('bds.crm_request_rental_user').id
            domain = [
                ('user_id.groups_id','=',user_rental_group_id)
            ]
        return {
            'domain':{
                'employee_id': domain
            }
        }

class CrmRequestRequestRuleSheet(models.Model):
    _name = 'crm.request.request.rule.sheet'
    _description = 'CRM Request Request Rule Sheet'
    _inherit = 'crm.product.request.rule.sheet'

    requirement = fields.Selection(string='Nhu cầu', selection=[(
        'rental', 'Cần thuê'), ('sale', 'Cần mua')], track_visibility='always')

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
    
    def _prepare_crm_request_line(self,crm_product_id):
        return {
            'employee_id': self.employee_id.id,
            'crm_product_id': crm_product_id.id,
            'requirement': crm_product_id.requirement,
            'is_show_attachment': True,
            'is_show_house_no': True,
            'is_show_email': True
        }

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
        mail_ids = []
        for user in user_ids:
            res = self._create_email_activity(user)
            mail_ids.append(res.id)
        self.update({
            'mail_ids': [(6,0,mail_ids)]
        })

    @api.multi
    def btn_approve(self):
        self.ensure_one()
        approver = self.env.user.employee_ids[0]
        self.update({
            'state': 'approved',
            'approved_date': datetime.now(),
            'approver': approver.id
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
                'approver': approver.id
            })
        self.make_action_done()
        self.send_notification('Đã duyệt bởi: {}'.format(approver.name))
               

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('crm.request.request.rule.sheet') or '/'
            vals['sequence'] = int(vals['name'].split('-')[1])
        res = super().create(vals)
        return res