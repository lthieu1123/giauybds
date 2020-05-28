from odoo import models, fields, api
from odoo import models, fields, api, exceptions
from datetime import datetime
from odoo.tools.translate import _

class EccAnnoucement(models.TransientModel):
    _name = 'announce'
    _description = 'Announce'

    def _get_default_message(self):
        return self.env.context.get('default_message', False)

    def _get_default_active_model(self):
        return self.env.context.get('default_active_model', False)

    def _get_default_active_id(self):
        return self.env.context.get('default_active_id', False)

    name = fields.Char('name', default=_get_default_message)
    active_model = fields.Char('Active Model', default=_get_default_active_model)
    active_id = fields.Integer('Active Id', default=_get_default_active_id)

    @api.multi
    def btn_open(self):
        self.ensure_one()
        context = self.env.context
        # active_model = context.get('default_active_model',False)
        # active_id = context.get('default_active_id',False)
        if not (self.active_model or self.active_id):
            raise exceptions.ValidationError(_('Something wrong happened, please contact with administrator.'))
        else:
            return {
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': False,
                'res_model': self.active_model,
                'res_id': self.active_id,
                'context': context,
                'target': 'current',
                'type': 'ir.actions.act_window'
            }