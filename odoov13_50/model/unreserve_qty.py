from odoo import api, models, fields, _, exceptions
import pdb

class StockPickingUnreserve(models.Model):
	_inherit = "stock.picking"



	def unreserve_qty(self):
		for move_line in self.move_line_ids_without_package:
			
			for abc in self.env['stock.quant'].search([('product_id','=',move_line.product_id.id),('location_id','=',self.location_id.id)]):
				abc.reserved_quantity = abc.reserved_quantity - move_line.product_uom_qty
				if abc.reserved_quantity < 0:
					abc.reserved_quantity = 0

			# pdb.set_trace()
			# new_val= move_line.product_uom_qty
			self.env.cr.execute(""" UPDATE stock_move_line SET product_uom_qty = 0, product_qty = 0 WHERE picking_id = %s ;""" % (tuple(self.ids) ))
			# move_line.write({
			# 		'product_qty': 0,
			# 		'product_qty': 0})
			# 
