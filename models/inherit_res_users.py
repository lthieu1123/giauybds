# -*- coding: utf-8 -*-

import json
import logging

from odoo import _, api, fields, models, registry, exceptions
from odoo.exceptions import UserError
from odoo.tools.translate import _
from odoo.addons import decimal_precision as dp
from ..commons.bds_constant import *
from datetime import datetime


class Base(models.AbstractModel):
    _inherit = 'base'

    @api.multi
    def export_data(self, fields_to_export, raw_data=False):
        """Only Admin can export data

        Args:
            fields_to_export ([type]): [description]
            raw_data (bool, optional): [description]. Defaults to False.

        Returns:
            [type]: [description]
        """
        if not self.env.user.has_group('base.group_system'):
            raise exceptions.ValidationError('Bạn không có quyền xuất dữ liệu')
        return super(Base, self).export_data(fields_to_export, raw_data)


class InheritResUsers(models.Model):
    _inherit = 'res.users'

    notification_type = fields.Selection(default='inbox')

    def __init__(self, pool, cr):
        """ Override of __init__ to add access rights on notification_email_send
            and alias fields. Access rights are disabled by default, but allowed
            on some specific fields defined in self.SELF_{READ/WRITE}ABLE_FIELDS.
        """
        init_res = super(InheritResUsers, self).__init__(pool, cr)
        # duplicate list to avoid modifying the original reference
        type(self).SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        type(self).SELF_WRITEABLE_FIELDS.extend(['notification_type'])
        # duplicate list to avoid modifying the original reference
        type(self).SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
        type(self).SELF_READABLE_FIELDS.extend(['notification_type'])
        return init_res


class InheritHrEmployee(models.Model):
    _inherit = 'hr.employee'

    def _validate_only_user(self):
        existed = self.search([
            ('user_id', '=', self.user_id.id),
            ('id', '!=', self.id if self.id else False)
        ])
        if existed.id:
            raise exceptions.ValidationError(
                'Đã có nhân viên cho người dùng: "{}". Vui lòng chọn người dùng khác.'.format(self.user_id.name))

    @api.onchange('user_id')
    def _onchange_user_id(self):
        if self.user_id.id:
            self._validate_only_user()

    @api.constrains('user_id')
    def _constrains_user_id(self):
        for rec in self:
            if rec.user_id.id:
                rec._validate_only_user()

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.user_id.id:
            res.user_id.write({
                'employee_id': res.id
            })
        return res

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        for rec in self:
            if rec.user_id.id:
                rec.user_id.write({'employee_id': rec.id})
        return res
