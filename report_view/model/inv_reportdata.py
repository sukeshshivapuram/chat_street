"""

"""
import time
from datetime import datetime, date, time, timedelta
import logging
from odoo import models, fields, api
# from datetime import date 
# from datetime import datetime,date,timedelta
from pytz import timezone
import pdb

class InvreportData(models.Model):

	_inherit = 'inventory.base.report'



	# push_data = fields.Boolean("Push",compute='push_datas',store=True)
	push_data1 = fields.Boolean("Push",compute='push_datas',store=True)



	# print(last_date,"***********^^^^^^^^^^^^^000000000000")




	@api.depends('product_id')
	def  push_datas(self):
		opening_qty = '''
			select 
	                product_id ,
	                ABS(sum(product_qty)) as qty,
	                ABS(sum(value)) as value
	        from 
	                inventory_base_report 
	        where 
	                date <= %s and 
	                product_id =%s and
	                (warehouse_id IS NULL or warehouse_id in %s  ) and
	                transaction_types NOT IN  ( 'internal' )

	        group by product_id,warehouse_id

		'''	

		# closing_qty = ''' 
		# 			select 
	 #                product_id ,
	 #                ABS(sum(product_qty)) as qty,
	 #                ABS(sum(value)) as value
	 #        from 
	 #                inventory_base_report 
	 #        where 
	 #                date <= %s and 
	 #                product_id =%s and
	 #                (warehouse_id IS NULL or warehouse_id in %s  ) and
	 #                transaction_types NOT IN  ( 'internal' )

	 #        group by product_id,warehouse_id

	 #        '''


	
		for each_line in self :
			if each_line and not each_line.push_data1:
				# if not each_line.warehouse_id.id:
				# 	pdb.set_trace()
				reportobject = self.env['data.for.reports']
				print("newwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
				curr_id = reportobject.search([('product_id','=',each_line.product_id.id),('warehouse_id','=',each_line.warehouse_id.id),('date','=',each_line.date.date())])
				print(curr_id.date,"****************************JKUTY*&IJOKJOI***************")
				if not curr_id:
					# pdb.set_trace()
					# last_date = each_line.date.date() -datetime.timedelta(days=1)	
					now_utc = datetime.now(timezone('UTC'))
					now_ist = now_utc.astimezone(timezone('Asia/Calcutta'))
					ist_date =now_ist.strftime("%Y-%m-%d")
					# print(ist_date)
					last_date = now_ist.date()
					print(last_date,"esiwuh4ti")




					closing_date = each_line.date.date()

					# closing_value_params = (each_line.date.date(),each_line.product_id.id,tuple(each_line.warehouse_id.ids,) if each_line.warehouse_id else (0,) )
					# self.env.cr.execute(closing_qty,closing_value_params)
					# clo_res = self.env.cr.dictfetchall()

					opening_value_params = (last_date,each_line.product_id.id,tuple(each_line.warehouse_id.ids,) if each_line.warehouse_id else (0,) )
					self.env.cr.execute(opening_qty,opening_value_params)
					op_res = self.env.cr.dictfetchall()

					open_qty = op_res[0]['qty'] if op_res else 0.0 
					open_val = op_res[0]['value'] if op_res else 0.0 

					# pdb.set_trace()
					vlas_list1={
					'product_id':each_line.product_id.id,
					'uom_id':each_line.product_id.uom_id.id,
					'category_id': each_line.product_id.categ_id.id,
					'product_code': each_line.product_id.default_code,
					'warehouse_id':  each_line.warehouse_id.id if each_line.warehouse_id else 0 ,
					'date':  each_line.date.date(),

					'sys_op_qty': op_res[0]['qty'] if op_res else 0.0,

					'sys_op_value': op_res[0]['value'] if op_res else 0.0,

					'gr_in_qty':  each_line.product_qty if each_line.transaction_types == 'p_receipt' else 0.0,
					'gr_in_value':   each_line.value if each_line.transaction_types == 'p_receipt' else 0.0,

					'grr_out_qty':  each_line.product_qty if each_line.transaction_types == 'p_return' else 0.0,
					'grr_out_val':   each_line.value if each_line.transaction_types == 'p_return' else 0.0,

					'selling_qty':  each_line.product_qty if each_line.transaction_types == 's_shipment' else 0.0,
					'selling_val':   each_line.value if each_line.transaction_types == 's_shipment' else 0.0,

					'consumed_qty':  each_line.product_qty if each_line.transaction_types == 'in' else 0.0,
					'consumed_val':   each_line.value if each_line.transaction_types == 'in' else 0.0,

					'to_in_qty':  each_line.product_qty if each_line.transaction_types == 't_receipt' else 0.0,
					'to_in_val':   each_line.value if each_line.transaction_types == 't_receipt' else 0.0,

					'to_out_qty':  each_line.product_qty if each_line.transaction_types == 't_shipment' else 0.0,
					'to_out_val':   each_line.value if each_line.transaction_types == 't_shipment' else 0.0,

					'intransit_qty': each_line.product_qty if each_line.transaction_types == 't_shipment' else 0.0,
					'intransit_val': each_line.value if each_line.transaction_types == 't_shipment' else 0.0,

					'variance_qty': each_line.product_qty if each_line.transaction_types == 'positive' else 0.0+ each_line.product_qty if each_line.transaction_types == 'negative' else 0.0,
					'variance_val': each_line.value if each_line.transaction_types == 'positive' else 0.0+ each_line.value if each_line.transaction_types == 'negative' else 0.0,

					'wastage_qty':(-(each_line.product_qty) if each_line.product_qty <0 else each_line.product_qty)if each_line.loss_reasons == 'wasted'  else 0.0,
					'wastage_val':(-(each_line.value) if each_line.value<0 else each_line.value)if each_line.loss_reasons =='wasted' else 0.0, 

					'damaged_qty':(-(each_line.product_qty) if each_line.product_qty<0 else each_line.product_qty) if each_line.loss_reasons == 'damaged' else 0.0,
					'damaged_val':(-(each_line.value) if each_line.value else each_line.value) if each_line.loss_reasons == 'damaged' else 0.0,

					'inventory_added_qty':(-(each_line.product_qty) if each_line.product_qty<0 else each_line.product_qty) if each_line.loss_reasons == 'inventory_added' else 0.0,
					'inventory_added_val':(-(each_line.value) if each_line.value<0 else each_line.value) if each_line.loss_reasons == 'inventory_added' else 0.0,

					'inventory_closing_qty':(-(each_line.product_qty) if each_line.product_qty<0 else each_line.product_qty) if each_line.loss_reasons == 'closing' else 0.0,
					'inventory_closing_val':(-(each_line.value if each_line.value<0 else each_line.value) if each_line.value<0 else each_line.value)if each_line.loss_reasons == 'closing' else 0.0,

					'expired_qty':(-(each_line.product_qty) if each_line.product_qty<0 else each_line.product_qty) if each_line.loss_reasons == 'expired' else 0.0,
					'expired_val':(-(each_line.value) if each_line.value<0 else each_line.value) if each_line.loss_reasons == 'expired' else 0.0,

					'inventory_sale_qty':(-(each_line.product_qty) if each_line.product_qty<0 else each_line.product_qty) if each_line.loss_reasons == 'sale' else 0.0,
					'inventory_sale_val':(-(each_line.value) if each_line.value<0 else each_line.value) if each_line.loss_reasons == 'sale' else 0.0,
					
					# 'sys_closing_qty': clo_res[0]['qty'] if clo_res else 0.0,

					# 'sys_closing_val': clo_res[0]['value'] if clo_res else 0.0,

					'sys_closing_qty': open_qty+ each_line.product_qty if each_line.transaction_types != 'internal' else 0.0,
										 # each_line.product_qty if each_line.transaction_types =='p_receipt' else 0.0+
					# 					each_line.product_qty if each_line.transaction_types =='p_return' else 0.0 +
					# 					each_line.product_qty if each_line.transaction_types =='s_shipment' else 0.0 +
					# 					each_line.product_qty if each_line.transaction_types =='in' else 0.0 +
					# 					each_line.product_qty if each_line.transaction_types =='out' else 0.0 +
					# 					each_line.product_qty if each_line.transaction_types =='t_receipt' else 0.0 +
					# 					each_line.product_qty if each_line.transaction_types =='t_shipment' else 0.0 +
					# 					each_line.product_qty if each_line.transaction_types =='positive' else 0.0 +
					
					# 					each_line.product_qty if each_line.transaction_types =='s_return' else 0.0 +
					# 					each_line.product_qty if each_line.transaction_types =='negative' else 0.0,

					'sys_closing_val': open_val+ 
										each_line.product_qty if each_line.transaction_types != 'internal' else 0.0,
										# 	each_line.value if each_line.transaction_types =='p_receipt' else 0.0+
										# each_line.value if each_line.transaction_types =='p_return' else 0.0 +
										# each_line.value if each_line.transaction_types =='s_shipment' else 0.0 +
										# each_line.value if each_line.transaction_types =='in' else 0.0 +
										# each_line.value if each_line.transaction_types =='out' else 0.0 +
										# each_line.value if each_line.transaction_types =='t_receipt' else 0.0 +
										# each_line.value if each_line.transaction_types =='t_shipment' else 0.0 +
										# each_line.value if each_line.transaction_types =='positive' else 0.0 +

										# each_line.value if each_line.transaction_types =='s_return' else 0.0 +
										# each_line.value if each_line.transaction_types =='negative' else 0.0,



					}
					new_id =reportobject.create(vlas_list1)
					print(vlas_list1,"rdoseirue985u90rue98673")
					each_line.write({'push_data1':True})
				else:
					print("sduiyse8tyeutwyhrge8tyurdfmklsdjf")
					update_qty={

					

						
					# if each_line.transaction_types == 'p_receipt':
						
					'gr_in_qty':  (curr_id.gr_in_qty+each_line.product_qty) if each_line.transaction_types == 'p_receipt' else curr_id['gr_in_qty'],
					'gr_in_value':   curr_id.gr_in_value+each_line.value if each_line.transaction_types == 'p_receipt' else curr_id['gr_in_value'],
						 
					# if  each_line.transaction_types == 'p_return':
						
					'grr_out_qty':  curr_id.grr_out_qty+each_line.product_qty if  each_line.transaction_types == 'p_return' else curr_id['grr_out_qty'],
					'grr_out_val':   curr_id.grr_out_val+each_line.value if  each_line.transaction_types == 'p_return' else curr_id['grr_out_val'],
							
					# if  each_line.transaction_types == 's_shipment':
						
					'selling_qty':  curr_id.selling_qty+each_line.product_qty if  each_line.transaction_types == 's_shipment' else curr_id['selling_qty'],
					'selling_val':   curr_id.selling_val+each_line.value if  each_line.transaction_types == 's_shipment' else curr_id['selling_val'],
							

					# if  each_line.transaction_types == 'in':
						
					'consumed_qty':  curr_id.consumed_qty+each_line.product_qty if  each_line.transaction_types == 'in' else curr_id['consumed_qty'],
					'consumed_val':   curr_id.consumed_val+each_line.value if  each_line.transaction_types == 'in' else curr_id['consumed_val'],
							

					# if  each_line.transaction_types == 't_receipt':
						
					'to_in_qty':  curr_id.to_in_qty+each_line.product_qty if  each_line.transaction_types == 't_receipt' else curr_id['to_in_qty'],
					'to_in_val':   curr_id.to_in_val+each_line.value if  each_line.transaction_types == 't_receipt' else curr_id['to_in_val'],
						
					# if each_line.transaction_types == 't_shipment':
						
					'to_out_qty':  curr_id.to_out_qty+each_line.product_qty if each_line.transaction_types == 't_shipment' else curr_id['to_out_qty'],
					'to_out_val':  curr_id.to_out_val+ each_line.value if each_line.transaction_types == 't_shipment' else curr_id['to_out_val'],
					
					'intransit_qty':curr_id.intransit_qty+each_line.product_qty if each_line.transaction_types == 't_shipment' else curr_id['to_out_qty'],
					'intransit_val': curr_id.intransit_val+ each_line.value if each_line.transaction_types == 't_shipment' else curr_id['to_out_val'],
					# if each_line.loss_reasons == 'wasted':
						
					'wastage_qty': (curr_id.wastage_qty+-(each_line.product_qty) if each_line.product_qty<0 else each_line.product_qty)if each_line.loss_reasons == 'wasted' else curr_id['wastage_qty'],
					'wastage_val': (curr_id.wastage_qty+-(each_line.value) if each_line.value<0 else each_line.value) if each_line.loss_reasons == 'wasted' else curr_id['wastage_val'],
						
					# if each_line.loss_reasons == 'damaged':
						# print("sjethgwu4twuitjbfsh")
						
					'damaged_qty':(curr_id.damaged_qty+-(each_line.product_qty) if each_line.product_qty<0 else each_line.product_qty)if each_line.loss_reasons == 'damaged' else curr_id['damaged_qty'],
					'damaged_val':(curr_id.damaged_val+-(each_line.value) if each_line.value<0 else each_line.value)if each_line.loss_reasons == 'damaged' else curr_id['damaged_val'],
						
					# if each_line.loss_reasons == 'inventory_added':
						# print("vvvvio0poppppppppu989789oooooooooo")
						
					'inventory_added_qty':(curr_id.inventory_added_qty+-(each_line.product_qty) if each_line.product_qty<0 else each_line.product_qty)if each_line.loss_reasons == 'inventory_added' else curr_id['inventory_added_qty'],
					'inventory_added_val':(curr_id.inventory_added_val+-(each_line.value) if each_line.value<0 else each_line.value)if each_line.loss_reasons == 'inventory_added' else curr_id['inventory_added_val'],
						
					# if each_line.loss_reasons == 'closing':
						
					'inventory_closing_qty':(curr_id.inventory_closing_qty+-(each_line.product_qty) if each_line.product_qty<0 else each_line.product_qty)if each_line.loss_reasons == 'closing' else curr_id['inventory_closing_qty'],
					'inventory_closing_val':(curr_id.inventory_closing_val+-(each_line.value) if each_line.value<0 else each_line.value)if each_line.loss_reasons == 'closing' else curr_id['inventory_closing_val'],
						
					# if each_line.loss_reasons == 'expired':
						
					'expired_qty':(curr_id.expired_qty+-(each_line.product_qty) if each_line.product_qty<0 else each_line.product_qty)if each_line.loss_reasons == 'expired' else curr_id['expired_qty'],
					'expired_val':(curr_id.expired_val+-(each_line.value) if each_line.value<0 else each_line.value)if each_line.loss_reasons == 'expired' else curr_id['expired_val'],
						
					# if each_line.loss_reasons == 'sale':
						
					'inventory_sale_qty':(curr_id.inventory_sale_qty+-(each_line.product_qty) if each_line.product_qty<0 else each_line.product_qty)if each_line.loss_reasons == 'sale' else curr_id['inventory_sale_qty'],
					'inventory_sale_val':(curr_id.inventory_sale_val+-(each_line.value) if each_line.value<0 else each_line.value)if each_line.loss_reasons == 'sale' else curr_id['inventory_sale_val'],

						
					# if each_line.transaction_types != 'internal':
						
					'sys_closing_qty':curr_id.sys_closing_qty + each_line.product_qty if each_line.transaction_types != 'internal' else curr_id['sys_closing_qty'],
					'sys_closing_val':curr_id.sys_closing_val + each_line.value if each_line.transaction_types != 'internal' else curr_id['sys_closing_val'],
						


					# if each_line.transaction_types == 'positive' or each_line.transaction_types == 'negative':
						
					'variance_qty': curr_id.variance_qty+each_line.product_qty if each_line.transaction_types == 'positive' or each_line.transaction_types == 'negative' else curr_id['variance_qty'],
					'variance_val': curr_id.variance_val+each_line.value if each_line.transaction_types == 'positive' or each_line.transaction_types == 'negative' else curr_id['variance_val'],
						
					
					'sys_op_qty':curr_id.sys_op_qty,
					'sys_op_value':curr_id.sys_op_value,
					}
						

					
					# 'sys_closing_qty':curr_id.sys_closing_qty,
					# 'sys_closing_qty':curr_id.sys_closing_qty,
						
					print(update_qty)					
					curr_id.write(update_qty)
					each_line.write({'push_data1':True})






























