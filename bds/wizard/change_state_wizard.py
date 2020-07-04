from odoo import models, fields, api
from odoo import models, fields, api, exceptions
from datetime import datetime
from odoo.tools.translate import _

class ApproveRejectProductWizard(models.TransientModel):
    _name = 'change.state.wizard'
    _description = 'Change Sate Wizard'

    def _get_default_crm_product(self):
        context = self.env.context
        ids = False
        if context.get('active_model','') == 'crm.product':
            ids = context.get('active_ids')
        return ids

    def _get_default_crm_request(self):
        context = self.env.context
        ids = False
        if context.get('active_model','') == 'crm.request':
            ids = context.get('active_ids')
        return ids

    state = fields.Many2one(string='Trạng thái',comodel_name='crm.states.product', default = lambda self: self.env.ref('bds.crm_state_open'), required=True)
    
    crm_product_ids = fields.Many2many(string='Sản phẩm',comodel_name='crm.product', default=_get_default_crm_product)
    crm_request_ids = fields.Many2many(string='Nhu cầu', comodel_name='crm.request', default=_get_default_crm_request)

    @api.multi
    def btn_apply(self):
        self.ensure_one()
        context = self.env.context.copy()
        msg = 'Đã chuyển {} {} sang trạng thái: "{}"'
        action = {
            'name': 'Thành công',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'announce',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': False,
        }
        if len(self.crm_product_ids):
            self.crm_product_ids.update({
                'state': self.state.id
            })
            context['default_message'] = msg.format(len(self.crm_product_ids),'sản phẩm',self.state.name)
            action.update({
                'context': context
            })
            return action
            
        if len(self.crm_request_ids):
            self.crm_request_ids.update({
                'state': self.state.id
            })
            context['default_message'] = msg.format(len(self.crm_request_ids),'nhu cầu',self.state.name)
            action.update({
                'context': context
            })
            return action
    
