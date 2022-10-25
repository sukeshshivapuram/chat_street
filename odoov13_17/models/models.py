from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError

class PurchaseApprovalMatrix(models.Model):
    _name = 'purchase.approval.matrix'

    product_category_id = fields.Many2one('product.category')
    value = fields.Integer()
    user_ids = fields.Many2many('res.users')


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_approve(self, force=False):
        cat = self.order_line[0].product_id.categ_id
        approval_ref = self.env['purchase.approval.matrix'].search([
                ('product_category_id','=',cat.id)])
        if approval_ref and self.amount_total > approval_ref.value and self.env.user not in approval_ref.user_ids:
            raise UserError(_('You are not authorized to approve PO of '+cat.name+' category'))
        self.write({'state': 'purchase', 'date_approve': fields.Date.context_today(self)})
        self.filtered(lambda p: p.company_id.po_lock == 'lock').write({'state': 'done'})
        return {}

    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()

            cat = order.order_line[0].product_id.categ_id
            # for line in order.order_line:
            #     if line.product_id.categ_id != cat:
            #         raise UserError(_('Can not confirm an order with products from different Categories'))

            approval_ref = self.env['purchase.approval.matrix'].search([
                ('product_category_id','=',cat.id)])
            if not approval_ref:
                order.button_approve()
            elif order.amount_total <= approval_ref.value or self.env.user in approval_ref.user_ids:
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
      
        return True