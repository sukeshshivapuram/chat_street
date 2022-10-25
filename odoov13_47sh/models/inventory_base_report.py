"""

"""
from odoo import models, fields, api
from datetime import datetime
import pdb

class InventoryBaseReport(models.Model):

	_name = 'inventory.base.report'
	_description='inventory.base.report'

	product_id = fields.Many2one('product.product', string="Product")
	move_id = fields.Many2one('stock.move', string="Move")
	uom_id = fields.Many2one('uom.uom', string="Uom")
	category_id = fields.Many2one('product.category', string="Category")
	warehouse_id = fields.Many2one('stock.warehouse',string='Warehouse')
	location_id = fields.Many2one('stock.location',string='Source')
	location_dest_id = fields.Many2one('stock.location',string='Destnation')
	product_code = fields.Char("Internal Reference")
	date=fields.Datetime(string="Date")
	# push_data = fields.Boolean("Push",compute='push_datas',store=True)
	# push_data1 = fields.Boolean("Push",compute='push_datas',store=True)
	# push_data3 = fields.Boolean('Push2',compute='push_opcldata',store=True)

	name = fields.Char("Name")
	product_qty=fields.Float("Qty")
	price_unit=fields.Float("Price")
	value=fields.Float("Value")
	loss_reasons = fields.Selection([
    ('expired', 'Expired'), 
    ('wasted', 'Wasted'),
    ('damaged', 'Damaged'),
    ('inventory_added', 'Inventory Added'), 
    ('closing', 'Closing'), 
    ('sale', 'Sale')],compute ='get_lossreason',store=True)
	# records_id = fields.Boolean('Record',)

	# Purchase retun 
	# Sales shipment 
	# Negative adjustiment 
	# Tranfer shipment 
	# Consumpution



	transaction_types = fields.Selection([
        ('p_receipt', 'Purchase Receipt'),
        ('p_return', 'Purchase Return'),
        ('positive', 'Positive Adjustment'),
        ('negative', 'Negative Adjustment'),
        ('s_shipment', 'Sales Shipment'),
        ('s_return', 'Sales Returns'),
        ('in', 'Consumpution'),
        ('out', 'Output'),
        ('t_shipment', 'Transfer Shipment'),
        ('t_receipt', 'Transfer Receipt'),
        ('internal', 'Internal Movement'),
        ], string='Transaction Type')


	@api.depends('move_id')
	def get_lossreason(self):
		print("cheeeeeeeeeeeeeeeeeeeeeeeeeeeeecl")
		for ls in self:
			if ls.move_id.loss_reason:
				ls.loss_reasons = ls.move_id.loss_reason	
			else:

				ls.loss_reasons = False







class StockQuant(models.Model):

	_inherit = 'stock.move'
	# z_price = fields.Float(compute='compute_product_price',store=True)
	data_sent = fields.Boolean(default=False,compute='compute_inventory_value',store=True)

	s_type = fields.Selection([
        ('supplier', 'Vendor Location'),
        ('view', 'View'),
        ('internal', 'Internal Location'),
        ('customer', 'Customer Location'),
        ('inventory', 'Inventory Loss'),
        ('production', 'Production'),
        ('transit', 'Transit Location')], string='Source Location Type',
        compute='compute_s_location_type',store=True)
	d_type = fields.Selection([
        ('supplier', 'Vendor Location'),
        ('view', 'View'),
        ('internal', 'Internal Location'),
        ('customer', 'Customer Location'),
        ('inventory', 'Inventory Loss'),
        ('production', 'Production'),
        ('transit', 'Transit Location')], string='Destnation Location Type',
        compute='compute_s_location_type',store=True)




	@api.depends('location_id','location_dest_id')
	def compute_s_location_type(self):
		for l in self:
			if l.location_id and l.location_dest_id:
				l.s_type =l.location_id.usage
				l.d_type =l.location_dest_id.usage
			else:
				l.s_type= False
				l.d_type= False




	@api.depends('state','picking_id.state')
	def compute_inventory_value(self):
		# inventory =[]
		for rec in self:
			# rec.ensure_one()
			# pdb.set_trace()
			if rec.state == 'done' and rec.picking_id.state == 'done' and rec.data_sent == False and (rec.s_type =='internal' or rec.d_type == 'internal'):
				# print(rec)
				InventoryObj = self.env['inventory.base.report']
				ValuationObj = self.env['stock.valuation.layer']
				valuation_query ='''select 
					sum(unit_cost) as unit,
					sum(quantity) as qty,
					sum(value) as va
				from  stock_valuation_layer
				 where stock_move_id = %s and 
					product_id = %s'''
				params = (rec.id,rec.product_id.id)

				self.env.cr.execute(valuation_query, params)
				result = self.env.cr.dictfetchall() 
				# valuation_id = ValuationObj.search([('stock_move_id','=',rec.id),('product_id','=',rec.product_id.id)])
				if rec.s_type == 'inventory':
					curr_transaction = 'positive'
				elif rec.d_type == 'inventory':
					curr_transaction ='negative'
				elif rec.s_type == 'supplier':
					curr_transaction ='p_receipt'
				elif rec.d_type =='supplier':
					curr_transaction ='p_return'
				elif rec.s_type == 'customer':
					curr_transaction ='s_return'
				elif rec.d_type =='customer' :
					curr_transaction ='s_shipment'
				elif rec.s_type == 'production':
					curr_transaction ='out'
				elif rec.d_type =='production':
					curr_transaction ='in'
				elif rec.s_type == 'transit':
					curr_transaction ='t_receipt'
				elif rec.d_type =='transit':
					curr_transaction ='t_shipment'
				elif rec.d_type == rec.s_type :
					curr_transaction = 'internal'
				else :
					curr_transaction = False

				# If the valuation is not thery we have to cosider the move
				if result[0]['va'] != None and  result[0]['qty']  != 0:
					curr_qty =result[0]['qty'] 
					price= result[0]['va']/curr_qty
					qty= curr_qty
					# print('SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')
				else:
					price= rec.z_price
					qty= rec.product_uom_qty
					# print('DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD')

				if rec.s_type =="internal" :
					w_code = rec.location_id.complete_name.split('/')[0]

					warehouse_id = self.env['stock.warehouse'].search([('code','=',w_code)])
					# print('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
				elif rec.s_type =="internal" and rec.d_type =="internal":
					w_code = rec.location_dest_id.complete_name.split('/')[0]
					warehouse_id = self.env['stock.warehouse'].search([('code','=',w_code)])
					# print('GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG')
				else:
					w_code = rec.location_dest_id.complete_name.split('/')[0]
					warehouse_id = self.env['stock.warehouse'].search([('code','=',w_code)])
					# print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH')
				if curr_transaction in ['t_shipment','in']:
					qty = -(abs(qty))

				# print(price,'*******************************8')

				vlas_list=[{
					'product_id':rec.product_id.id,
					'uom_id':rec.product_uom.id,
					'category_id': rec.product_id.categ_id.id,
					'product_code': rec.product_id.default_code,
					'warehouse_id':  warehouse_id.id if warehouse_id else False,
					'product_qty':  -(abs(qty)) if  curr_transaction in ['t_shipment','in','negative'] else qty,
					'price_unit': price,
					'location_id': rec.location_id.id,
					'location_dest_id': rec.location_dest_id.id,
					'transaction_types': curr_transaction,
					'date': rec.date,
					'value': qty*price,
					'move_id':rec.id					

				}]
				# print(check,"weurftwirywi4ryiwywi8rfy")
				# check = vlas_list[0]['move_id'] == vlas_list[0]['move_id'] and vlas_list[0]['price_unit'] == 0
				# print(vlas_list)
				# if vlas_list[0]['move_id'] == vlas_list[0]['move_id']  and vlas_list[0]['price_unit'] != 0:
				new_id =InventoryObj.create(vlas_list)
				rec.data_sent = True
				# print(new_id,'*****************new id1')
				# elif check:
				# 	# if check:
				# 	new_id =InventoryObj.create(vlas_list)
				# 	print(new_id,'*****************new id2')
				# 	inventory.append(new_id)

			# print(inventory,'********************************8')
			elif rec.inventory_id and rec.data_sent == False:
				InventoryObj = self.env['inventory.base.report']
				ValuationObj = self.env['stock.valuation.layer']
				valuation_query ='''select 
					sum(unit_cost) as unit,
					sum(quantity) as qty,
					sum(value) as va
				from  stock_valuation_layer
				 where stock_move_id = %s and 
					product_id = %s'''
				params = (rec.id,rec.product_id.id)

				self.env.cr.execute(valuation_query, params)
				result = self.env.cr.dictfetchall() 
				# valuation_id = ValuationObj.search([('stock_move_id','=',rec.id),('product_id','=',rec.product_id.id)])
				if rec.s_type == 'inventory':
					curr_transaction = 'positive'
				elif rec.d_type == 'inventory':
					curr_transaction ='negative'
				elif rec.s_type == 'supplier':
					curr_transaction ='p_receipt'
				elif rec.d_type =='supplier':
					curr_transaction ='p_return'
				elif rec.s_type == 'customer':
					curr_transaction ='s_return'
				elif rec.d_type =='customer' :
					curr_transaction ='s_shipment'
				elif rec.s_type == 'production':
					curr_transaction ='out'
				elif rec.d_type =='production':
					curr_transaction ='in'
				elif rec.s_type == 'transit':
					curr_transaction ='t_receipt'
				elif rec.d_type =='transit':
					curr_transaction ='t_shipment'
				elif rec.d_type == rec.s_type :
					curr_transaction = 'internal'
				else :
					curr_transaction = False

				# If the valuation is not thery we have to cosider the move
				if result[0]['va'] != None and  result[0]['qty']  != 0:
					curr_qty =result[0]['qty'] 
					price= result[0]['va']/curr_qty
					qty= curr_qty
					# print('SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')
				else:
					price= rec.z_price
					qty= rec.product_uom_qty
					# print('DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD')

				if rec.s_type =="internal" :
					w_code = rec.location_id.complete_name.split('/')[0]

					warehouse_id = self.env['stock.warehouse'].search([('code','=',w_code)])
					# print('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
				elif rec.s_type =="internal" and rec.d_type =="internal":
					w_code = rec.location_dest_id.complete_name.split('/')[0]
					warehouse_id = self.env['stock.warehouse'].search([('code','=',w_code)])
					# print('GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG')
				else:
					w_code = rec.location_dest_id.complete_name.split('/')[0]
					warehouse_id = self.env['stock.warehouse'].search([('code','=',w_code)])
					# print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH')
				if curr_transaction in ['t_shipment','in']:
					qty = -(abs(qty))

				# print(price,'*******************************8')

				vlas_list=[{
					'product_id':rec.product_id.id,
					'uom_id':rec.product_uom.id,
					'category_id': rec.product_id.categ_id.id,
					'product_code': rec.product_id.default_code,
					'warehouse_id':  warehouse_id.id if warehouse_id else False,
					'product_qty':  -(abs(qty)) if  curr_transaction in ['t_shipment','in','negative'] else qty,
					'price_unit': price,
					'location_id': rec.location_id.id,
					'location_dest_id': rec.location_dest_id.id,
					'transaction_types': curr_transaction,
					'date': rec.date,
					'value': qty*price,
					'move_id':rec.id					

				}]
				# print(check,"weurftwirywi4ryiwywi8rfy")
				# check = vlas_list[0]['move_id'] == vlas_list[0]['move_id'] and vlas_list[0]['price_unit'] == 0
				# print(vlas_list)
				# if vlas_list[0]['move_id'] == vlas_list[0]['move_id']  and vlas_list[0]['price_unit'] != 0:
				new_id =InventoryObj.create(vlas_list)
				rec.data_sent = True



			# print("InventoryObjInventoryObjInventoryObjInventoryObj",new_id)




class StockValuationLayer22(models.Model):


	_inherit = 'stock.valuation.layer'

	data_sent = fields.Boolean(default=False,compute='compute_inventory_values',store=True)

	@api.depends('stock_move_id')
	def compute_inventory_values(self):
		for l in self:
			InventoryObj = self.env['inventory.base.report']
			ValuationObj = self.env['stock.valuation.layer']
			if l.stock_landed_cost_id:


				query ='''select 

					ABS(sum(quantity)) as qty,
					ABS(sum(value)) as va
				from  stock_valuation_layer
				 where stock_move_id = %s and 
					product_id = %s'''

				params = (l.stock_move_id.id,l.product_id.id)

				self.env.cr.execute(query, params)
				result = self.env.cr.dictfetchall() 
				# valuvation_ids =ValuationObj.search([('stock_move_id','=',l.stock_move_id.id),('product_id','=',l.product_id.id),('remaining_value','=',True)])
				curr_id = InventoryObj.search([('move_id','=',l.stock_move_id.id)])
				
				curr_id.write({	
								'value' : result[0]['va'],
								'price_unit' : result[0]['va']/result[0]['qty']
								})
				# print("beforeddddddddddddddddddd",valuvation_ids,curr_id,tot_val)


























