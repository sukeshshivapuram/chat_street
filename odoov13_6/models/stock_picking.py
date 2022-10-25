from odoo import api, fields, models,_
from odoo.exceptions import UserError


class PickingType(models.Model):
    _inherit = "stock.picking.type"


    putaway = fields.Boolean(
        'Putaway Scan Required', default=False)


class Picking(models.Model):
    _inherit = "stock.picking"
    putaway = fields.Boolean(related='picking_type_id.putaway', store=True)

    # suggested_bin_id= fields.Many2one('stock.location','Suggested Bins',compute='onchange_product')

    # @api.depends('product_id')
    # def onchange_product(self):
    # 	# stock_summary = self.env['stock.quant'].search([('location_id.is_bin','=',True)])
    # 	# no_stock = True
    # 	line_id =self.env['stock.quant'].search([('product_id','=',self.product_id.id)], order="id desc", limit=1)
    # 	self.suggested_bin_id = line_id.location_id.id


    def button_validate(self):
        res = super(Picking, self).button_validate()
        if self.picking_type_id.putaway == True:
            for line in self.move_line_ids_without_package:
                if not line.location_dest_id.is_bin == True:
                    raise UserError(_('Please Select Bin location for putaway operations.'))
        return res


    def get_barcode_view_state(self):
        """ Return the initial state of the barcode view as a dict.
        """
        fields_to_read = self._get_picking_fields_to_read()
        pickings = self.read(fields_to_read)
        for picking in pickings:

            picking['move_line_ids'] = self.env['stock.move.line'].browse(picking.pop('move_line_ids')).read([
                'product_id',
                'location_id',
                'location_dest_id',
                'qty_done',
                'display_name',
                'product_uom_qty',
                'product_uom_id',
                'product_barcode',
                'owner_id',
                'lot_id',
                'lot_name',
                'package_id',
                'result_package_id',
                'dummy_id',
                # 'suggested_bin_id',
                'suggested_bin_loc',
                'putaway',
            ])
            
         
            for move_line_id in picking['move_line_ids']:
                move_line_id['product_id'] = self.env['product.product'].browse(move_line_id.pop('product_id')[0]).read([
                    'id',
                    'tracking',
                    'barcode',
                ])[0]
                move_line_id['location_id'] = self.env['stock.location'].browse(move_line_id.pop('location_id')[0]).read([
                    'id',
                    'display_name',
                ])[0]
                move_line_id['location_dest_id'] = self.env['stock.location'].browse(move_line_id.pop('location_dest_id')[0]).read([
                    'id',
                    'display_name',
                ])[0]
            picking['location_id'] = self.env['stock.location'].browse(picking.pop('location_id')[0]).read([
                'id',
                'display_name',
                'parent_path'
            ])[0]
            picking['location_dest_id'] = self.env['stock.location'].browse(picking.pop('location_dest_id')[0]).read([
                'id',
                'display_name',
                'parent_path'
            ])[0]
            

            picking['group_stock_multi_locations'] = self.env.user.has_group('stock.group_stock_multi_locations')
            picking['group_tracking_owner'] = self.env.user.has_group('stock.group_tracking_owner')
            picking['group_tracking_lot'] = self.env.user.has_group('stock.group_tracking_lot')
            picking['group_production_lot'] = self.env.user.has_group('stock.group_production_lot')
            picking['group_uom'] = self.env.user.has_group('uom.group_uom')
            picking['use_create_lots'] = self.env['stock.picking.type'].browse(picking['picking_type_id'][0]).use_create_lots
            picking['use_existing_lots'] = self.env['stock.picking.type'].browse(picking['picking_type_id'][0]).use_existing_lots
            picking['show_entire_packs'] = self.env['stock.picking.type'].browse(picking['picking_type_id'][0]).show_entire_packs
            picking['actionReportDeliverySlipId'] = self.env.ref('stock.action_report_delivery').id
            picking['actionReportBarcodesZplId'] = self.env.ref('stock.action_label_transfer_template_zpl').id
            picking['actionReportBarcodesPdfId'] = self.env.ref('stock.action_label_transfer_template_pdf').id
            if self.env.company.nomenclature_id:
                picking['nomenclature_id'] = [self.env.company.nomenclature_id.id]
        return pickings

    def _get_picking_fields_to_read(self):
        """ Return the default fields to read from the picking.
        """
        return [
            'move_line_ids',
            'picking_type_id',
            'location_id',
            'location_dest_id',
            'name',
            'state',
            'picking_type_code',
            'company_id',
            'putaway',
        ]



class StockMoveLine(models.Model):
    _inherit= 'stock.move.line'
    # suggested_bin_id= fields.Many2one('stock.location','Suggested Bins')
    suggested_bin_loc = fields.Char('suggested bin location', compute='onchange_product')

    putaway = fields.Boolean(related='picking_id.picking_type_id.putaway', store=True)

    @api.depends('product_id')
    def onchange_product(self):
    # stock_summary = self.env['stock.quant'].search([('location_id.is_bin','=',True)])
    # no_stock = True
    # pdb.set_trace()

        # default_id = self.env['stock.location'].search([('is_default_loc','=',True)])
        if self.product_id:
            for each_product in self.product_id:
                line_id = self.env['stock.quant'].search([('product_id','=',each_product.id),('location_id.is_bin','=', True)], order="id desc", limit=1)

                if line_id.location_id.is_bin:

                    location = self.env['stock.location'].search([('id','=',line_id.location_id.id)])
                    self.suggested_bin_loc = location.complete_name
                else:

                    self.suggested_bin_loc = 'No Previous Records Found'
        else:
            self.suggested_bin_loc = 'No Previous Records Found'






    def get_suggested_bin(self, productid):

        line_id =self.env['stock.quant'].search([('product_id','=',productid),('location_id.is_bin','=', True)], order="id desc", limit=1)
        if line_id.location_id.is_bin:

            location = self.env['stock.location'].search([('id','=',line_id.location_id.id)])
            return location.complete_name
        else:

            return 'No Previous Records Found'


class StockLocation(models.Model):
    _inherit = "stock.location"

    is_bin = fields.Boolean("Is a Putaway location?")
    # is_default_loc = fields.Boolean("Is a default Suggestion?")





