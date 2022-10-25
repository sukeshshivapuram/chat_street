# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import api, fields, models, SUPERUSER_ID, _


class StockLocation(models.Model):
    _inherit = "stock.location"

    is_bin = fields.Boolean("Is a Bin?")
    is_kic = fields.Boolean("Is in Kitchen")
    kc_ref = fields.Char("Kitchen location code")
    is_staff_location = fields.Boolean("Is a Staff Location?")
    daily_staff_budget = fields.Float(string='Daily Staff Budget')
    amt_consumed = fields.Float()


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    is_putaway = fields.Boolean("Is Putaway")
    validate_done_qty = fields.Boolean("Validate Done Quantities")


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    is_putaway = fields.Boolean(string="Is Putaway",related="picking_type_id.is_putaway",store=True)

    def set_locations(self):
        stock_summary = self.env['stock.quant'].search([('location_id.is_bin','=',True)])
        no_stock = True

        for line in self.move_line_ids_without_package:
            
            for stock in stock_summary:
                if line.product_id.id == stock.product_id.id:
                    line.location_dest_id = stock.location_id.id
                    no_stock = False
                    break
            
            if no_stock:
                stock_locations = [stock.location_id.id for stock in stock_summary]
                locations = self.env['stock.location'].search([('is_bin','=',True)])
                
                for location in locations:
                    if location.id not in stock_locations:
                        line.location_dest_id = stock.location_id.id
                        break

    def button_validate(self):

        if self.location_dest_id.is_staff_location:
            total = 0
            avail = self.location_dest_id.daily_staff_budget - self.location_dest_id.amt_consumed
            for line in self.move_ids_without_package:
                total += line.product_id.standard_price * line.qty_done
            if total > avail:
                raise ValidationError(_("Out of staff consumption limit\namount remaining : %s"%avail))
            else:
                self.location_dest_id.amt_consumed += total
        return super(StockPicking,self).button_validate()