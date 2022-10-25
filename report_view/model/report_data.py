from odoo import api, models, fields, _, exceptions
from datetime import datetime
import pdb



class ReportData(models.Model):
	_name='data.for.reports'
	_description = "data.for.reports"



	product_id = fields.Many2one('product.product', string="Product")
	move_id = fields.Many2one('stock.move', string="Move")
	uom_id = fields.Many2one('uom.uom', string="Uom")
	category_id = fields.Many2one('product.category', string="Category")
	warehouse_id = fields.Many2one('stock.warehouse',string='Warehouse')
	# location_id = fields.Many2one('stock.location',string='Source')
	# location_dest_id = fields.Many2one('stock.location',string='Destnation')
	product_code = fields.Char("Internal Reference")
	date=fields.Datetime(string="Date")
	name = fields.Char("Name")
	product_qty=fields.Float("Qty")
	price_unit=fields.Float("Price")
	value=fields.Float("Value")
	data_sent = fields.Boolean(default=False)


	sys_op_qty = fields.Float("Sys Opening Qty")
	sys_op_value = fields.Float("Sys Opening Value")

	gr_in_qty = fields.Float("Gr In Qty")
	gr_in_value = fields.Float("Gr In Value")


	to_in_qty = fields.Float("To In Qty")
	to_in_val = fields.Float("To In Value")

	to_out_qty = fields.Float("To Out Qty")
	to_out_val = fields.Float("To Out Value")


	grr_out_qty = fields.Float("GRR Out Qty")
	grr_out_val = fields.Float("GRR In Value")

	intransit_qty = fields.Float("Intransit Qty")
	intransit_val = fields.Float("Intransit Value")


	wastage_qty = fields.Float("Wastage Qty")
	wastage_val = fields.Float("Wastage Value")


	expired_qty = fields.Float("Expired Qty")
	expired_val = fields.Float("Expired Value")

	damaged_qty = fields.Float("Damaged Qty")
	damaged_val = fields.Float("Damaged Value")

	inventory_added_qty = fields.Float("Inventory Added")
	inventory_added_val = fields.Float("Inventory Value")

	inventory_closing_qty = fields.Float("Closing  Qty")
	inventory_closing_val = fields.Float("Closing Value")

	inventory_sale_qty = fields.Float("Sale Qty")
	inventory_sale_val = fields.Float("Sale Value")

	variance_qty = fields.Float("Variance Qty")
	variance_val = fields.Float("Variance Value")

	consumed_qty = fields.Float("Consumed Qty")
	consumed_val = fields.Float("Consumed Value")

	selling_qty = fields.Float("Selling Qty")
	selling_val = fields.Float("SellingValue")

	sys_closing_qty = fields.Float("Sys Closing Qty")
	sys_closing_val = fields.Float("Sys Closing Value")

	actual_cons = fields.Float("Actual Consumption")
	closing_map = fields.Float("Closing MAP")

	# grr_in_qty = fields.Float("GRR Out Qty")
	# grr_in_val = fields.Float("GRR Out Value")

