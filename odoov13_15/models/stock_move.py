from odoo.tools.float_utils import float_is_zero, float_compare
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import Warning
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp
import datetime
from datetime import datetime

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    show_dest_stock = fields.Boolean(compute="_get_stock_visibility",store=True)

    @api.depends('picking_type_id')
    def _get_stock_visibility(self):
        for rec in self:
            if rec.picking_type_id.code == 'internal':
                rec.show_dest_stock = True
            else:
                rec.show_dest_stock = False

class StockMove(models.Model):
    _inherit = 'stock.move'

    mrp_indent_stock_line_id = fields.Many2one('indent.order', 'Material Requisition')
    stock_indent_stock_line_id = fields.Many2one('stock.indent.order', 'Material Requisition')
    indent_line_id = fields.Many2one('indent.order.line',
        'Material Requisition Order Line', ondelete='set null', index=True, readonly=True, copy=False)
    stock_indent_line_id = fields.Many2one('stock.indent.order.line',
        'Stock Material Requisition Order Line', ondelete='set null', index=True, readonly=True, copy=False)
    created_indent_line_id = fields.Many2one('indent.order.line',
        'Created Material Requisition Order Line', ondelete='set null', readonly=True, copy=False)
    stock_created_indent_line_id = fields.Many2one('stock.indent.order.line',
        'Created Stock Material Requisition Order Line', ondelete='set null', readonly=True, copy=False)
    dest_stock = fields.Float(compute='_get_dest_stock')
    show_dest_stock = fields.Boolean(compute='_get_dest_stock')

    @api.depends('product_id')
    def _get_dest_stock(self):
        for rec in self:
            qty = 0
            if rec.picking_id.location_dest_id.is_kic and rec.picking_id.show_dest_stock:
                qty = self.env['aggregated.inventory'].search([
                                            ('product_ref','=',rec.product_id.default_code),
                                            ('warehouse_ref','=',rec.picking_id.location_dest_id.kc_ref)]).quantity
            rec.dest_stock = qty