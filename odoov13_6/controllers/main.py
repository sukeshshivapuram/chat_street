from odoo import http, _
from odoo.http import request
from odoo.addons.stock_barcode.controllers.main import StockBarcodeController

class StockBarcodeController(StockBarcodeController):

	@http.route('/stock_barcode/scan_from_main_menu1', type='json', auth='user')
	def create_putaway_py(self):
	    """ If barcode represent a picking type, open a new
	    picking with this type
	    """
	    picking_type = request.env['stock.picking.type'].search([
	        ('putaway', '=', 'True'),
	    ], limit=1)
	    if picking_type:
	        # Find source and destination Locations
	        location_dest_id, location_id = picking_type.warehouse_id._get_partner_locations()
	        if picking_type.default_location_src_id:
	            location_id = picking_type.default_location_src_id
	        if picking_type.default_location_dest_id:
	            location_dest_id = picking_type.default_location_dest_id

	        # Create and confirm the picking
	        picking = request.env['stock.picking'].create({
	            'user_id': False,
	            'picking_type_id': picking_type.id,
	            'location_id': location_id.id,
	            'location_dest_id': location_dest_id.id,
	            'immediate_transfer': True,
	        })

	        return  self.get_action(picking.id)
	    return {'warning': _('Please Check for Putawy Operations')}



	@http.route(['/get_suggested_bin'], type='json', auth="user")

	def get_suggested_bin(self, **kw):

		#Fetch input json data sent from js

		productid = kw.get('productid')

		line_id =request.env['stock.quant'].search([('product_id','=',productid),('location_id.is_bin','=', True)], order="id desc", limit=1)
		if line_id.location_id.is_bin:

		    location = request.env['stock.location'].search([('id','=',line_id.location_id.id)])
		    return location.complete_name
		else:

		    return 'No Previous Records Found'


		# # Your code is here 


		# return {

		# 'output_data' : output_data

		# }


