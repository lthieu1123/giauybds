from odoo import models, fields, api
from odoo import models, fields, api, exceptions
from datetime import datetime
from odoo.tools.translate import _

class ApproveRejectProductWizard(models.TransientModel):
    _name = 'approve.reject.product.wizard'
    _description = 'Approve Reject Product Wizard'

    def _get_default_approver(self):
        return self.env.user.employee_ids.ids[0]

    def _get_model_ids(self):
        context = self.env.context.copy()
        if context.get('active_model',False) == 'crm.product.request.rule.sheet' and context.get('active_ids',False):
            return context.get('active_ids')

    approver_id = fields.Many2one(comodel_name='hr.employee', string='Người duyệt', default=_get_default_approver)
    model_ids = fields.Many2many(comodel_name='crm.product.request.rule.sheet',string='model_ids', default=_get_model_ids)
    line_ids = fields.Many2many(comodel_name='approve.reject.product.line.wizard',inverse_name='approve_reject_product_id',string='Danh sách sản phẩm cần duyệt')

    @api.onchange('model_ids')
    def _onchange_model_ids(self):
        self.line_ids = False
        if len(self.model_ids):
            values = []
            for item in self.model_ids:
                vals = self.env['approve.reject.product.line.wizard']._prepare_line_id(self.id,item)
                values.append((0, 0, vals))
            self.line_ids = values
    
    @api.multi
    def btn_apply(self):
        for line in line_ids:
            pass



class ApproveRejectProductLineWizard(models.TransientModel):
    _name = 'approve.reject.product.line.wizard'
    _description = 'Approve Reject Product Line Wizard'

    def _get_default_id(self):
        return self.env.context.get('default_id', False)

    approve_reject_product_id = fields.Many2one(comodel_name='approve.reject.product.wizard',string='Model ID',default=_get_default_id)
    crm_product_id = fields.Many2one(comodel_name='crm.product',string='Sản phẩm',ondelete='cascade')
    approve = fields.Boolean('Duyệt',default=True)


    def _prepare_line_id(self,parent_id,line_id):
        vals = {
            'approve_reject_product_id': parent_id,
            'crm_product_id': line_id.id,
            'approve': True
        }
        return vals
