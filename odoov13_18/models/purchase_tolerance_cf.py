from odoo import fields, models,api,_
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

class Purchasetoleranceinventry(models.Model):
    _inherit='product.template'

    z_purchase_tolerance = fields.Float(string='Purchase Tolerance',default=0.0,required=True)
    purchase_tol_reqd = fields.Boolean(string='Purchase Tolerance Required?',)
# class Purchasetolerancepurchase(models.Model):
#     _inherit='product.supplierinfo'

#     zy_purchase_tolerance = fields.Float(string='Purchase Tolerance',default=0.0,required=True)


class Purchasetolerancevariants(models.Model):
    _inherit = 'product.product'

    zx_purchase_tolerance = fields.Float(string='Purchase Tolerance',default=0.0,required=True)


class Validatepurchasetolerance(models.Model):
    _inherit = "stock.picking"

    @api.depends('move_line_ids_without_package', 'stock.move', 'stock.move.line')
    # @api.multi
    def button_validate(self):
        self.ensure_one()
        if not self.move_lines and not self.move_line_ids:
            raise UserError(_('Please add some items to move.'))
        # if self.move_line_nosuggest_ids:
        #     for line in self.move_line_nosuggest_ids:
        #         if line.qty_done > line.product_uom_qty:
        #             for vendor_line in self.product_id.variant_seller_ids:
        #                 if vendor_line.name == self.partner_id:
        #                     if vendor_line.zy_purchase_tolerance != 0:
        #                         if line.qty_done > (line.product_uom_qty + vendor_line.zy_purchase_tolerance):
        #                             raise UserError(_('Done quantity is more than requested quantity'))
        #             if self.product_id:
        #                 if self.product_id.zx_purchase_tolerance != 0:
        #                     if line.qty_done > (line.product_uom_qty + self.product_id.zx_purchase_tolerance):
        #                         raise UserError(_('Done quantity is more than requested (product.product) quantity')) 
        #             if self.product_id:
        #                 if self.product_id.z_purchase_tolerance != 0:
        #                     if line.qty_done > (line.product_uom_qty + self.product_id.z_purchase_tolerance):
        #                         raise UserError(_('Done quantity is more than requested (product.template) quantity'))


        if self.move_ids_without_package and self.picking_type_id.code!='internal':
            for line in self.move_ids_without_package:
                if line.quantity_done > line.product_uom_qty:
                #     for vendor_line in self.product_id.variant_seller_ids:
                #         if vendor_line.name == self.partner_id:
                #             if vendor_line.zy_purchase_tolerance != 0:
                #                 if line.quantity_done > (line.product_uom_qty + vendor_line.zy_purchase_tolerance):
                #                     raise UserError(_('Done quantity is more than requested quantity'))
                #     if self.product_id:
                #         if self.product_id.zx_purchase_tolerance != 0:
                #             if line.quantity_done > (line.product_uom_qty + self.product_id.zx_purchase_tolerance):
                #                 raise UserError(_('Done quantity is more than requested (product.product) quantity')) 
                #     for order_line in self:
                    
                        # if line.product_id.z_purchase_tolerance != 0:
                        if line.product_id.purchase_tol_reqd == True:
                            
                            if (line.quantity_done - line.product_uom_qty) > line.product_id.z_purchase_tolerance:
                                raise UserError(_('GR quantity is greater than PO quantity for {}. You can do {} {} of extra GR over the PO quantity.'.format(line.product_id.name,line.product_id.z_purchase_tolerance,line.product_id.uom_id.name)))
                        # elif self.product_id.zx_purchase_tolerance != 0:
                        #     if line.qty_done-line.product_uom_qty > (line.product_uom_qty/100) * self.product_id.zx_purchase_tolerance:
                        #         raise UserError(_('Done quantity is more than requested quantity inventry purchase'))                        

        # If no lots when needed, raise error
        picking_type = self.picking_type_id
        precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        no_quantities_done = all(float_is_zero(move_line.qty_done, precision_digits=precision_digits) for move_line in self.move_line_ids)
        no_reserved_quantities = all(float_is_zero(move_line.product_qty, precision_rounding=move_line.product_uom_id.rounding) for move_line in self.move_line_ids)
        if no_reserved_quantities and no_quantities_done:
            raise UserError(_('You cannot validate a transfer if no quantites are reserved nor done. To force the transfer, switch in edit more and encode the done quantities.'))

        if picking_type.use_create_lots or picking_type.use_existing_lots:
            lines_to_check = self.move_line_ids
            if not no_quantities_done:
                lines_to_check = lines_to_check.filtered(
                    lambda line: float_compare(line.qty_done, 0,
                                               precision_rounding=line.product_uom_id.rounding)
                )

            for line in lines_to_check:
                product = line.product_id
                if product and product.tracking != 'none':
                    if not line.lot_name and not line.lot_id:
                        raise UserError(_('You need to supply a Lot/Serial number for product %s.') % product.display_name)

        if no_quantities_done:
            view = self.env.ref('stock.view_immediate_transfer')
            wiz = self.env['stock.immediate.transfer'].create({'pick_ids': [(4, self.id)]})
            return {
                'name': _('Immediate Transfer?'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'stock.immediate.transfer',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': wiz.id,
                'context': self.env.context,
            }

        if self._get_overprocessed_stock_moves() and not self._context.get('skip_overprocessed_check'):
            view = self.env.ref('stock.view_overprocessed_transfer')
            wiz = self.env['stock.overprocessed.transfer'].create({'picking_id': self.id})
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'stock.overprocessed.transfer',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': wiz.id,
                'context': self.env.context,
            }

        # Check backorder should check for other barcodes
        if self._check_backorder():
            return self.action_generate_backorder_wizard()
        self.action_done()
        return
