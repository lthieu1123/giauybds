# -*- coding: utf-8 -*-

from odoo import api, fields, models

class CrmStatesProduct(models.Model):
    _name = 'crm.states.product'
    _description = 'CRM States BDS'

    name = fields.Char('State')
    sequence = fields.Integer(default=1)
    fold = fields.Boolean(string='Folded in Kanban', default=False,
                          help='This stage is folded in the kanban view when there are no records in that stage '
                               'to display.')

class CrmStatesRequest(models.Model):
    _name = 'crm.states.request'
    _description = 'CRM States BDS'

    name = fields.Char('State')
    sequence = fields.Integer(default=1)
    fold = fields.Boolean(string='Folded in Kanban', default=False,
                          help='This stage is folded in the kanban view when there are no records in that stage '
                               'to display.')


class CrmCity(models.Model):
    _name = 'crm.city'
    _description = 'CRM State BDS'

    name = fields.Char('City')
    country = fields.Many2one('res.country','Country')