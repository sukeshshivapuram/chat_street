# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import api, fields, models, SUPERUSER_ID, _



class ProductTemplate(models.Model):
    _inherit = 'product.template'

    z_hsn_code = fields.Char("HSN Code")



class StockPicking(models.Model):
    _inherit = 'stock.picking'

    z_driver = fields.Char("Driver Name")
    z_contact = fields.Char("Contact Number")
    z_vehicle = fields.Char("Vehicle Number")
    z_dispatch = fields.Datetime("Dispatch Time")

    def calculste_sto_qty(self,product):
        print(self.purchase_id.id,666666666666666666)

        for record in self.move_ids_without_package:
            
            simba = self.env['purchase.order'].search([('id','=',self.purchase_id.id),('order_line.product_id','=',record.product_id.id)])
            # print("\n"*5,simba)
            # print(simba.order_line)
            thor = simba.order_line
            emp_list=[]
            for linez in thor:
                if product.id==linez.product_id.id:
                    hulk = linez.product_qty
                    emp_list.append(hulk)
                    # print(emp_list,1111111111111111111111111111)
                    return emp_list