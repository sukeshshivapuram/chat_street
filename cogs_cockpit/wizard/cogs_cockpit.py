# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.



import io
import locale
import base64
import textwrap
from copy import copy

from datetime import datetime,timedelta
from openpyxl import Workbook
from odoo import models, fields, api,_
from openpyxl.drawing.image import Image
from openpyxl.drawing.xdr import XDRPositiveSize2D
from openpyxl.utils.units import pixels_to_EMU, cm_to_EMU
from odoo.exceptions import UserError, ValidationError,Warning
from openpyxl.drawing.spreadsheet_drawing import OneCellAnchor, AnchorMarker
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font, colors
import pdb

class CogsReport(models.TransientModel):
    _name = "cogs.cockpit"
    _description = "cogs.cockpit"

    date_start = fields.Date(string="Start Date")
    date_end = fields.Date(string="End Date", default=fields.Datetime.now)


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
    report_data_id = fields.Many2one('data.for.reports', string="Cockpit id")


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



    # @api.constrains('date_start')
    # def _code_constrains(self):
    #     if self.date_start > self.date_end:
    #         raise ValidationError(_("'Start Date' must be before 'End Date'"))
    # Get the product and category filters 

    

    def generate_report(self):

        tree_view_id = self.env.ref('cogs_cockpit.view_cogs_cockpit_tree').id
        form_view_id = self.env.ref('cogs_cockpit.cogscockpit_view_form').id
        pivot_view_id = self.env.ref('cogs_cockpit.view_pivot_cogs_cockpit').id
        graph_view_id = self.env.ref('cogs_cockpit.cogs_cockpit_graph').id

        

        # opening_value_query = '''
        # select 
        #         product_id ,
        #         ABS(sum(product_qty)) as qty,
        #         ABS(sum(value)) as value
        # from 
        #         inventory_base_report 
        # where 
        #         date < %s and 
        #         product_id =%s and
        #         (warehouse_id in %s or warehouse_id is null) and
        #         transaction_types NOT IN  ( 'internal' )

        # group by product_id,warehouse_id

        # '''

        

        # closing_value_query = '''
        #     select 
        #             product_id ,
        #             ABS(sum(product_qty)) as qty,
        #             ABS(sum(value)) as value
        #     from 
        #             inventory_base_report 
        #     where 
        #             date <= %s and 
        #             product_id =%s and
        #             (warehouse_id in %s  or warehouse_id is null) and
        #             transaction_types NOT IN  ( 'internal' )

        #     group by product_id,warehouse_id

        #     '''


        # opening_qty = '''
        #     select 
        #             product_id ,
        #             sum(product_qty) as qty,
        #             sum(value)as value
        #     from 
        #             inventory_base_report 
        #     where 
        #             date < %s and 
        #             product_id =%s and
        #             (warehouse_id IS NULL or warehouse_id in %s  ) and
        #             transaction_types NOT IN  ( 'internal' )

        #     group by product_id,warehouse_id

        # '''    

        # closing_qty = '''
        #     select 
        #             product_id ,
        #             sum(product_qty) as qty,
        #             sum(value)as value
        #     from 
        #             inventory_base_report 
        #     where 
        #             date < %s and 
        #             product_id =%s and
        #             (warehouse_id IS NULL or warehouse_id in %s  ) and
        #             transaction_types NOT IN  ( 'internal' )

        #     group by product_id,warehouse_id


        # ''' 
        all_data_query = '''
            select  product_id,warehouse_id,
                    
               
                    sum(gr_in_qty) as gr_in_qty,
                    sum(gr_in_value) as gr_in_value,
                    sum(to_in_qty) as to_in_qty,
                    sum(to_in_val) as to_in_val,
                    sum(to_out_qty) as to_out_qty,
                    sum(to_out_val) as to_out_val,
                    sum(grr_out_qty) as grr_out_qty,
                    sum(grr_out_val) as grr_out_val,
                    sum(consumed_qty) as consumed_qty,
                    sum(consumed_val) as consumed_val,
                    sum(selling_qty) as selling_qty,
                    sum(selling_val) as selling_val,
                    sum(variance_qty) as variance_qty,
                    sum(variance_val) as variance_val,
                    sum(wastage_qty) as wastage_qty,
                    sum(wastage_val) as wastage_val,
                    sum(damaged_qty) as damaged_qty,
                    sum(damaged_val) as damaged_val,
                    sum(inventory_added_qty) as inventory_added_qty,
                    sum(inventory_added_val) as inventory_added_val,
                    sum(inventory_closing_qty) as inventory_closing_qty,
                    sum(inventory_closing_val) as inventory_closing_val,
                    sum(expired_qty) as expired_qty,
                    sum(expired_val) as expired_val,
                    sum(inventory_sale_qty) as inventory_sale_qty,
                    sum(inventory_sale_val) as inventory_sale_val
                 



            from   
                    data_for_reports 
            where 
                    
                    date <%s 

            group by product_id,warehouse_id 
                     
                    
            '''  

        data_range_query = '''
            select  product_id,warehouse_id,

                           
                    
                    sum(gr_in_qty) as gr_in_qty,
                    sum(gr_in_value) as gr_in_value,
                    sum(to_in_qty) as to_in_qty,
                    sum(to_in_val) as to_in_val,
                    sum(to_out_qty) as to_out_qty,
                    sum(to_out_val) as to_out_val,
                    sum(grr_out_qty) as grr_out_qty,
                    sum(grr_out_val) as grr_out_val,
                    sum(consumed_qty) as consumed_qty,
                    sum(consumed_val) as consumed_val,
                    sum(selling_qty) as selling_qty,
                    sum(selling_val) as selling_val,
                    sum(variance_qty) as variance_qty,
                    sum(variance_val) as variance_val,
                    sum(wastage_qty) as wastage_qty,
                    sum(wastage_val) as wastage_val,
                    sum(damaged_qty) as damaged_qty,
                    sum(damaged_val) as damaged_val,
                    sum(inventory_added_qty) as inventory_added_qty,
                    sum(inventory_added_val) as inventory_added_val,
                    sum(inventory_closing_qty) as inventory_closing_qty,
                    sum(inventory_closing_val) as inventory_closing_val,
                    sum(expired_qty) as expired_qty,
                    sum(expired_val) as expired_val,
                    sum(inventory_sale_qty) as inventory_sale_qty,
                    sum(inventory_sale_val) as inventory_sale_val
                 
                  
            from   
                    data_for_reports 
            where 
                    
                    date >=%s and
                    date <=%s

            group by product_id,warehouse_id 
                     
                    
            '''  

        all_opening_qry = '''
                         select 
                                product_id,warehouse_id,
                                sys_op_qty as sys_op_qty,
                                sys_op_value as sys_op_value,
                                sys_closing_qty as sys_closing_qty,
                                sys_closing_val as sys_closing_val                                
                            from 
                                data_for_reports
                            where
                                date <=%s and
                                product_id = %s and
                                warehouse_id =%s

                     

                            order by date Desc


                                   '''

        data_opening_query = '''
                         select 
                                product_id,warehouse_id,
                                sys_op_qty as sys_op_qty,
                                sys_op_value as sys_op_value,
                                sys_closing_qty as sys_closing_qty,
                                sys_closing_val as sys_closing_val                                
                            from 
                                data_for_reports
                            where
                                date >=%s and
                                date <=%s and
                                product_id = %s and
                                warehouse_id =%s

                                '''


        all_data_params = (self.date_start,)
        self.env.cr.execute(all_data_query,all_data_params)
        all_data_result = self.env.cr.dictfetchall()


        data_range_params = (self.date_start,self.date_end)
        self.env.cr.execute(data_range_query,data_range_params)
        data_range_result = self.env.cr.dictfetchall()  






        # all_data_result=self.env['data.for.reports'].search([('date','>=' ,self.date_start),('date','<' ,self.date_end)])
        # all_data_product=self.env['data.for.reports'].search([('date','<' ,self.date_start)])
        all_data_trans=self.env['data.for.reports'].search([('date','<' ,self.date_end)],order ="date desc")
        found_recs = {}
        

        self.env.cr.execute('''delete from cogs_cockpit where id is not null''')
        # pdb.set_trace()
        for result in data_range_result:
            obj_c = self.env['cogs.cockpit']
            curr_id = obj_c.search([('product_id','=',result['product_id']),('warehouse_id','=',result['warehouse_id'])])

            if not curr_id:


                closing_value_params = (self.date_start,self.date_end,result['product_id'],(result['warehouse_id'],) if result['warehouse_id'] else (0,) )
                self.env.cr.execute(data_opening_query,closing_value_params)
                clo_res = self.env.cr.dictfetchall()
            # if result['date']>=self.date_start:
                # opening_value_params = (self.date_start,result['product_id'],(result['warehouse_id'],) if result['warehouse_id'] else (0,) )
                # self.env.cr.execute(opening_qty,opening_value_params)
                # op_res = self.env.cr.dictfetchall()

                # closing_value_params = (self.date_end,result['product_id'],(result['warehouse_id'],) if result['warehouse_id'] else (0,) )
                # self.env.cr.execute(closing_qty,closing_value_params)
                # clo_res = self.env.cr.dictfetchall()
                
                vals ={
                    'product_id':result['product_id'],
                    # 'category_id':result['product_id'],
                    # 'uom_id':result['product_id'],
                    'warehouse_id':result['warehouse_id'],
                    'product_code':result['product_id'],
                    'name':result['product_id'],
                    'sys_op_qty':clo_res[0]['sys_op_qty'] if clo_res else 0.0,
                    'sys_op_value':clo_res[0]['sys_op_value'] if clo_res else 0.0,
                    'sys_closing_qty':clo_res[0]['sys_closing_qty'] if clo_res else 0.0,
                    'sys_closing_val':clo_res[0]['sys_closing_val'] if clo_res else 0.0, 
                    'gr_in_qty':result['gr_in_qty'],
                    'gr_in_value':result['gr_in_value'],
                    'to_in_qty':result['to_in_qty'],
                    'to_in_val':result['to_in_val'],
                    'to_out_qty':result['to_out_qty'],
                    'to_out_val':result['to_out_val'],
                    'grr_out_qty':result['grr_out_qty'],
                    'grr_out_val':result['grr_out_val'],
                    'consumed_qty':result['consumed_qty'],
                    'consumed_val':result['consumed_val'],
                    'selling_qty':result['selling_qty'],
                    'selling_val':result['selling_val'],
                    'variance_qty':result['variance_qty'],
                    'variance_val':result['variance_val'],
                    'wastage_qty':result['wastage_qty'],
                    'wastage_val':result['wastage_val'],
                    'expired_qty':result['expired_qty'],
                    'expired_val':result['expired_val'],
                    'damaged_qty':result['damaged_qty'],
                    'damaged_val':result['damaged_val'],
                    'inventory_added_qty':result['inventory_added_qty'],
                    'inventory_added_val':result['inventory_added_val'],
                    'inventory_closing_qty':result['inventory_closing_qty'],
                    'inventory_closing_val':result['inventory_closing_val'],
                    'inventory_sale_qty':result['inventory_sale_qty'],
                    'inventory_sale_val':result['inventory_sale_val'],

                }
                obj_c.create(vals)

        for result_remain in all_data_result:


                # pdb.set_trace()
            # found_recs.update({'product_id': result_remain['product_id'], 'warehouse_id':result_remain['warehouse_id']})
            curr_id = obj_c.search([('product_id','=',result_remain['product_id']),('warehouse_id','=',result_remain['warehouse_id'])])
            # if (result['product_id'],result['warehouse_id']) not in found_recs:
            if not curr_id :
                opening_value_params = (self.date_start,result_remain['product_id'],(result_remain['warehouse_id'],) if result_remain['warehouse_id'] else (0,) )
                self.env.cr.execute(all_opening_qry,opening_value_params)
                op_res = self.env.cr.dictfetchall()   

                # closing_value_params = (self.date_end,result_remain['product_id'],(result_remain['warehouse_id'],) if result_remain['warehouse_id'] else (0,) )
                # self.env.cr.execute(closing_qty,closing_value_params)
                # clo_res = self.env.cr.dictfetchall()             
                # pdb.set_trace()
                vals1 ={
                    'product_id':result_remain['product_id'],
                    # 'category_id':result.category_id.id,
                    # 'uom_id':result.uom_id.id,
                    'warehouse_id':result_remain['warehouse_id'],
                    'product_code':result_remain['product_id'],
                    'name':result_remain['product_id'],
                    'sys_op_qty':op_res[0]['sys_op_qty'] if op_res else 0.0,
                    'sys_op_value':op_res[0]['sys_op_value'] if op_res else 0.0,
                    'sys_closing_qty':op_res[0]['sys_closing_qty'] if op_res else 0.0,
                    'sys_closing_val':op_res[0]['sys_closing_val'] if op_res else 0.0,                    


                }
                obj_c.create(vals1)

            
            


        # remain_products =set(all_data_product.ids)-set(all_data_result.ids)
        # print(remain_products)





        # obj_c=self.env['cogs.cockpit']

        # self.env.cr.execute('''delete from cogs_cockpit where id is not null''')


        # for result in all_data_result:
        #     # print("resssssssssssssssssss",result)
                
        #     # if result.product_id.id in all_data_product.ids:

        #     opening_value_params = (self.date_start,result.product_id.id,tuple(result.warehouse_id.ids,))
        #     self.env.cr.execute(opening_value_query,opening_value_params)
        #     op_res = self.env.cr.dictfetchall()
            


        #     cclosing_value_params = (self.date_end,result.product_id.id,tuple(result.warehouse_id.ids,))
        #     self.env.cr.execute(closing_value_query,cclosing_value_params)
        #     clo_res = self.env.cr.dictfetchall()   

            


        #     vals ={
        #         'product_id':result.product_id.id,
        #         'category_id':result.category_id.id,
        #         'uom_id':result.uom_id.id,
        #         'warehouse_id':result.warehouse_id.id,
        #         'product_code':result.product_code,
        #         'name':result.name,
        #         'sys_op_qty':op_res[0]['qty'] if op_res else 0.0,
        #         'sys_op_value':op_res[0]['value'] if op_res else 0.0,
        #         'sys_closing_qty':clo_res[0]['qty'] if clo_res else 0.0,
        #         'sys_closing_val':clo_res[0]['value'] if clo_res else 0.0,
        #         'gr_in_qty':result.gr_in_qty,
        #         'gr_in_value':result.gr_in_value,
        #         'to_in_qty':result.to_in_qty,
        #         'to_in_val':result.to_in_val,
        #         'to_out_qty':result.to_out_qty,
        #         'to_out_val':result.to_out_val,
        #         'grr_out_qty':result.grr_out_qty,
        #         'grr_out_val':result.grr_out_val,
        #         'consumed_qty':result.consumed_qty,
        #         'consumed_val':result.consumed_val,
        #         'selling_qty':result.selling_qty,
        #         'selling_val':result.selling_val,
        #         'variance_qty':result.variance_qty,
        #         'variance_val':result.variance_val,
        #     }


    
        #     obj_c.create(vals)

        # for each_remain in remain_products:
        #     pdb.set_trace()
        #     record_exists = self.env['data.for.reports'].search([('id','=',each_remain)])
        #     record_not_exists = self.env['cogs.cockpit'].search([('report_data_id','=',each_remain)])
        #     if not record_not_exists:
        #         opening_pa = (self.date_start,record_exists.product_id.id,tuple(record_exists.warehouse_id.ids,))
        #         self.env.cr.execute(opening_value_query,opening_pa)
        #         op_res_1 = self.env.cr.dictfetchall()
                


        #         cclosing_p = (self.date_end,record_exists.product_id.id,tuple(record_exists.warehouse_id.ids,))
        #         self.env.cr.execute(closing_value_query,cclosing_p)
        #         clo_res_1 = self.env.cr.dictfetchall()   



        #         vals_1={
        #         'product_id':record_exists.product_id.id,
        #         'category_id':record_exists.category_id.id,
        #         'uom_id':record_exists.uom_id.id,
        #         'warehouse_id':record_exists.warehouse_id.id,
        #         'product_code':record_exists.product_code,
        #         'name':record_exists.name,
        #         'sys_op_qty':op_res_1[0]['qty'] if op_res_1 else 0.0,
        #         'sys_op_value':op_res_1[0]['value'] if op_res_1 else 0.0,
        #         'sys_closing_qty':clo_res_1[0]['qty'] if clo_res_1 else 0.0,
        #         'sys_closing_val':clo_res_1[0]['value'] if clo_res_1 else 0.0,
        #         }
        #         obj_c.create(vals_1)
        #         print("ddddddddddddddddddddd")


        return {
            'name': 'COGS COCKPIT',
            'view_mode': 'tree',
            'views': [[tree_view_id, 'tree'],[form_view_id, 'form'],[pivot_view_id, 'pivot'],[graph_view_id,'graph']],
            'res_model': 'cogs.cockpit',
            'type': 'ir.actions.act_window',
            'target': 'current',
            }
    