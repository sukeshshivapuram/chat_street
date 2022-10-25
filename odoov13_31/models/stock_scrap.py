# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, _

from odoo.exceptions import UserError,ValidationError

_logger = logging.getLogger(__name__)

class StockScrap(models.Model):
    _inherit = 'stock.scrap'


    @api.constrains('z_location_id','scrap_location_id')
    def _check_locations(self):

        if self.z_location_id.id != self.scrap_location_id.location_id.id:
            raise ValidationError(_("Please configure the scrap location "))

        




    lot_ids = fields.Many2many('stock.production.lot')
    z_location_ids = fields.Many2many('stock.location')
    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial',
        states={'done': [('readonly', True)]}, domain="[('product_id', '=', product_id), ('company_id', '=', company_id),('id','in', lot_ids)]", check_company=True)
    location_id = fields.Many2one(
        'stock.location', 'Source Location', domain="[ ('company_id', 'in', [company_id, False]),('id','in', z_location_ids)]",
        required=True, states={'done': [('readonly', True)]}, check_company=True)
    z_location_id = fields.Many2one('stock.location')
    scrap_location_id = fields.Many2one(
        'stock.location', 'Scrap Location',
        domain="[('scrap_location', '=', True), ('company_id', 'in', [company_id, False]),('location_id','=',z_location_id)]", required=True, states={'done': [('readonly', True)]}, check_company=True)


    @api.onchange('z_location_id')
    def get_domaine(self):
        if self.location_id:
            self.z_location_id = self.location_id.location_id.id


class StockPicking(models.Model):
    _inherit = 'stock.picking'



    def button_scrap(self):
        self.ensure_one()
        view = self.env.ref('stock.stock_scrap_form_view2')
        products = self.env['product.product']
        lot = self.env['stock.production.lot']
        loc = self.env['stock.location']
        for move in self.move_lines:
            if move.state not in ('draft', 'cancel') and move.product_id.type in ('product', 'consu'):
                products |= move.product_id

        lot_ids =[]
        loc_des_ids= []
        for each in self.move_line_ids_without_package:
            lot |= each.lot_id
            loc |= each.location_dest_id


        return {
            'name': _('Scrap'),
            'view_mode': 'form',
            'res_model': 'stock.scrap',
            'view_id': view.id,
            'views': [(view.id, 'form')],
            'type': 'ir.actions.act_window',
            'context': {'default_picking_id': self.id, 'product_ids': products.ids,'default_lot_ids': [(6, 0, lot.ids)], 'default_z_location_ids': [(6, 0, loc.ids)],'default_company_id': self.company_id.id},
            'target': 'new',
        }

    




