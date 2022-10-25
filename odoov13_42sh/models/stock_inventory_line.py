# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import pdb

class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    loss_reason = fields.Selection([
        ('expired', 'Expired'), 
        ('wasted', 'Wasted'),
        ('damaged', 'Damaged'),
        ('inventory_added', 'Inventory Added'), 
        ('closing', 'Closing'), 
        ('sale', 'Sale')])



class stockMove(models.Model):
    _inherit = "stock.move"




    loss_reason = fields.Selection([
        ('expired', 'Expired'), 
        ('wasted', 'Wasted'),
        ('damaged', 'Damaged'),
        ('inventory_added', 'Inventory Added'), 
        ('closing', 'Closing'), 
        ('sale', 'Sale')],compute='get_loss',store=True)


    @api.depends('inventory_id')
    def get_loss(self):
        for each in self:
            if each.inventory_id:
                

                query='''select 
                            sl.loss_reason as lr from stock_inventory_line as sl

                        where 
                            sl.inventory_id=%s and
                            sl.product_id=%s and 
                            (sl.location_id=%s or sl.location_id=%s)
                            
                            
                        
                        '''
                
                
                
                params = (each.inventory_id.id, each.product_id.id, each.location_id.id, each.location_dest_id.id)

                self.env.cr.execute(query,params)
                result = self.env.cr.dictfetchall()
               



                if result:

                    for loss_result in result:
                        each.loss_reason = loss_result['lr']


            else:
                each.loss_reason =False


class stockMoveLine(models.Model):

    _inherit = "stock.move.line"




    loss_reason = fields.Selection([
    ('expired', 'Expired'), 
    ('wasted', 'Wasted'),
    ('damaged', 'Damaged'),
    ('inventory_added', 'Inventory Added'), 
    ('closing', 'Closing'), 
    ('sale', 'Sale')],compute='get_loss_from_mv',store=True)


    @api.depends('move_id')
    def get_loss_from_mv(self):
        for each in self:
            if each.move_id and each.move_id.loss_reason:
                each.loss_reason = each.move_id.loss_reason
                
            else:
                each.loss_reason =False


