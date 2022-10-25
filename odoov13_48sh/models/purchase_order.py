# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from odoo import api, models, fields, _
from odoo.exceptions import AccessError, UserError, ValidationError



class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def check_receipt_date(self):
        today = fields.Date.today()
        for po in self.search([('state', '!=', 'cancel')]):
            if po.date_planned and datetime.date(po.date_planned) + timedelta(days=+2) < today:
                pickings = po.picking_ids.filtered(lambda p: p.state != 'done')
                if pickings and len(po.picking_ids) == 1:
                    pickings.mapped('move_lines').write({'state': 'cancel'})
                    pickings.action_cancel()
                    po.button_cancel()
                elif pickings:
                    pickings.mapped('move_lines').write({'state': 'cancel'})
                    pickings.action_cancel()

class StockPicking(models.Model):
    _inherit='stock.picking'

    def button_validate(self):
        res=super(StockPicking,self).button_validate()
        if self.purchase_id and not self.message_attachment_count:
            raise UserError(_('Attachment is missing'))
        return res    

                    

                    
