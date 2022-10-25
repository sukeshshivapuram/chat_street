from odoo import api, fields, models, SUPERUSER_ID, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    state = fields.Selection(selection_add=[
        ('closed','Closed'),
    ])

    closed = fields.Boolean(compute='check_close',store=True)
    cron_close = fields.Boolean()

    def reopen(self):
        self.state = 'purchase'

    @api.depends('order_line','order_line.qty_received','order_line.product_qty')
    def check_close(self):
        for rec in self:
            rec.closed = True
            for line in rec.order_line:
                if line.qty_received < line.product_qty:
                    rec.closed = False
                    break
            if rec.closed:
                rec.state = 'closed'

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
        'closed': [('readonly', True)],
    }

    date_order = fields.Datetime('Order Date', required=True, states=READONLY_STATES, index=True, copy=False, default=fields.Datetime.now,\
        help="Depicts the date where the Quotation should be validated and converted into a purchase order.")
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True, states=READONLY_STATES, change_default=True, tracking=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", help="You can find a vendor by its Name, TIN, Email or Internal Reference.")
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, states=READONLY_STATES,
        default=lambda self: self.env.company.currency_id.id)
    order_line = fields.One2many('purchase.order.line', 'order_id', string='Order Lines', states=READONLY_STATES, copy=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, states=READONLY_STATES, default=lambda self: self.env.company.id)


    def scheduled_po_closure(self):
        twodaysback = datetime.now() - timedelta(days = 2)
        for po in self.env['purchase.order'].search([('date_planned','<=',twodaysback),('closed','=',False)]):
            po.closed = po.cron_close = True
            po.state = 'closed'

# class PurchaseOrderLine(models.Model):
#     _inherit = "purchase.order.line"

#     @api.onchange('qty_received')
#     def compare_qty(self):
#         self.order_id.closed += 1

#         print('onchange(\'qty_received\')\n'*10,self.order_id.closed,'\n'*10)