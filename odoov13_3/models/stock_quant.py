# -*- coding: utf-8 -*-

from odoo import api, fields, models

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    life_date = fields.Datetime(related='lot_id.life_date', store=True, readonly=False)

    warehouse_id = fields.Many2one('stock.warehouse', store=True,compute='get_warehouse')



    @api.depends('product_id','location_id')
    def get_warehouse(self):
    	for each in self:
    		if each.location_id:
	    		curr_id =each.location_id.parent_path.split("/")
	    		if curr_id[0]:

	    			loca_id=self.env['stock.location'].search([('id','=',curr_id[1])])
	    			ware_id=self.env['stock.warehouse'].search([('code','=',loca_id.name)])
	    			each.warehouse_id = ware_id.id
	    		else:
	    			each.warehouse_id= False
	    	else:
	    		each.warehouse_id= False


