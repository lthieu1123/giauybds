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


class CrmCity(models.Model):
    _name = 'crm.district'
    _description = 'CRM State BDS'

    name = fields.Char('Tên')
    code = fields.Char('Code')
    state_id = fields.Many2one('res.country.state', 'Tỉnh/TP')
    country_id = fields.Many2one('res.country', 'Quốc gia')


class CrmWard(models.Model):
    _name = 'crm.ward'
    _description = 'CRM ward BDS'

    name = fields.Char('Tên', required=True)
    code = fields.Char('Code')
    country_id = fields.Many2one('res.country', 'Quốc gia')
    state_id = fields.Many2one('res.country.state', 'Tỉnh/TP')
    district_id = fields.Many2one('crm.district', 'Quận/Huyện')


class CrmStreet(models.Model):
    _name = 'crm.street'
    _description = 'CRM Street'

    name = fields.Char('Tên', required=True)
    code = fields.Char('Code')
    district_id = fields.Many2one('crm.district', 'Quận/Huyện')
    state_id = fields.Many2one('res.country.state', 'Tỉnh/TP')
    country_id = fields.Many2one('res.country', 'Quốc gia')

    @api.model
    def _change_all_data_to_no_update(self):
        _li_model = ['crm.street','crm.ward','crm.district','res.country.state']
        for model in _li_model:
            ids = self.env[model].search([]).ids
            self.env['ir.model.data'].search([
                    ('model','=',model),
                    ('res_id','in',ids),
                    ('module','=','bds')
                ]).write({'noupdate': True})