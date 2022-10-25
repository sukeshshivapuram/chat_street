from odoo import models, fields, api
from datetime import date

class StoFields(models.Model):
	_inherit='inter.company.transfer.line.ept'

	
	qty_done_dc = fields.Float(string='GRN Qty',related='delivered_qty')
	qty_deliver_dc = fields.Float(string='DC Qty',compute='_get_dc_qty')
	
	@api.depends('inter_company_transfer_id.picking_ids.state')
	def _get_dc_qty(self):
		for line in self:
			qty_deliver_dc = 0.0
			if line.inter_company_transfer_id.state == 'processed':
				for picking_id in line.inter_company_transfer_id.picking_ids.filtered(
                        lambda x: x.state != 'cancel' and x.picking_type_id.code == 'outgoing'):
					for move in picking_id.move_ids_without_package:
						if line.product_id == move.product_id:
							qty_deliver_dc += move.product_id.uom_id._compute_quantity(
                                move.quantity_done, move.product_id.uom_id)
			line.qty_deliver_dc = qty_deliver_dc


class ResUsers(models.Model):
    _inherit = 'res.users'

    sto_warehouse_line = fields.One2many('sto.warehouse.line','z_user_id',"From")



class StoWarehouseLine(models.Model):
    _name = "sto.warehouse.line"
    _description ="sto.warehouse.line"


    z_user_id = fields.Many2one('res.users')
    from_warehouse_id = fields.Many2one('stock.warehouse',"From")
    to_warehouse_ids = fields.Many2many('stock.warehouse','stock_warehouse_sto' )
    operation_ids = fields.Many2many(
        'stock.picking.type', 'stock_picking_type_sto'
        , string='Default Warehouse Operations')



class StoFieldsPicking(models.Model):
	_inherit='inter.company.transfer.ept'

	
	pick_out = fields.Char(string='DC Reference')
	pick_in = fields.Char(string='GRN Reference')
	eff_grn_dt = fields.Date(string='Effective GRN Date')
	eff_del_dt = fields.Date(string='Effective Delivery Date')
	# @api.depends('name')
	# def get_out_name(self):
	# 	for line in self:
	# 		if line.name:
	# 			var = self.env['stock.picking'].search([('origin','=',line.name)])
	# 			for l in var:
	# 				line.pick_out=l.name
	
	@api.depends('name','state')
	def get_in_name(self):

		for rec in self:
			if rec.name and rec.state !='draft':
				for line in self:
				
				
					# if line.name:
					# if line.state not in 'draft':
						# if line.id:
					var = self.env['stock.picking'].search(['&',('inter_company_transfer_id','=',line.id),('picking_type_id.code','=','incoming')])
					for l in var:
						line.pick_in=l.name
			else:
				rec.pick_in = False

	@api.depends('name','state')
	def get_out_name(self):
		for rec in self:
			if rec.name and rec.state != 'draft':
				for line in self:
				
				
					# if line.name:
					# if line.state not in 'draft':
						# if line.name:
					var = self.env['stock.picking'].search(['&',('inter_company_transfer_id','=',line.id),('picking_type_id.code','=','outgoing')])
					for l in var:
						line.pick_out=l.name
			else:
				rec.pick_out = False
	@api.depends('name','state')
	def get_del_dt(self):
		for rec in self:
			if rec.name and rec.state != 'draft':
				for line in self:
				
				
					# if line.name:
					# if line.state not in 'draft':
						# if line.name:
					var = self.env['stock.picking'].search(['&',('inter_company_transfer_id','=',line.id),('picking_type_id.code','=','outgoing')])
					for l in var:
						line.eff_del_dt=l.date_done
			else:
				rec.eff_del_dt = False
	@api.depends('name','state')
	def get_grn_dt(self):
		for rec in self:
			if rec.name and rec.state != 'draft':
				for line in self:
					var = self.env['stock.picking'].search([('inter_company_transfer_id','=',line.id),('picking_type_id.code','=','incoming')])
					for l in var:
						line.eff_grn_dt=l.date_done
			else:
				rec.eff_grn_dt = False