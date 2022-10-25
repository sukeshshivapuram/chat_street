"""
For inter_company_transfer_ept module.
"""
from odoo import fields, api, models,_
from odoo.exceptions import ValidationError,UserError
import pdb

class Picking(models.Model):
   
    _inherit = 'stock.picking'

    inter_company_transfer_id = fields.Many2one('inter.company.transfer.ept', string="ICT",
                                                copy=False, help="Reference of ICT.")

    # icd_no = fields.Many2many('stock.picking')


    ict_id_no = fields.Many2one('stock.picking',string="DC#", domain="[('picking_type_id.code', '=', 'outgoing')]", copy=False,help="Reference of STO.")
    
    op_code = fields.Selection([
        ('incoming','1'),
        ('outgoing','2'),
        ('internal','3')],related='picking_type_id.code')

    partner_id_helpers = fields.Many2one('res.partner',compute='get_partner_for_receipt',store=True)

    z_qty_count = fields.Boolean("Count")
    z_button_inv = fields.Boolean("Invisible")


    def _create_backorder(self):
        res = super(Picking, self)._create_backorder()
        for backorder in res:
            if backorder.backorder_id and backorder.backorder_id.inter_company_transfer_id:
                backorder.write({"inter_company_transfer_id":backorder.backorder_id.\
                                 inter_company_transfer_id.id,
                                 'z_button_inv': False})
        return res



    @api.depends('inter_company_transfer_id','picking_type_id')
    def get_partner_for_receipt(self):
        for l in self:
            if l.picking_type_id.code == 'incoming' and l.inter_company_transfer_id:
                l.partner_id_helpers = l.inter_company_transfer_id.source_warehouse_id.partner_id.id
                l.partner_id = l.inter_company_transfer_id.source_warehouse_id.partner_id.id
            else:
                l.partner_id_helpers =False


    def fetch_detailed_operation(self):

        picking = self.env['stock.picking'].search([
            ('inter_company_transfer_id','=',self.inter_company_transfer_id.id),
            ('op_code','=','outgoing')])
        if picking:
            
            move_count = 0
            

            for move in picking.move_ids_without_package:
                if len(move.move_line_ids)>1:

                    for move_line in move.move_line_ids:
                        
                        if move_line.state == 'done' and move_line.z_done == False :

                            current_move = self.env['stock.move'].search([('picking_id','=',self.id),('product_id','=',move_line.product_id.id)])

                            if current_move.product_uom_qty != move_line.qty_done and current_move.product_uom_qty >= move_line.qty_done  :
                                new_move_line = {
                                    'move_id':current_move.id,
                                    'product_id':move_line.product_id.id,
                                    'product_uom_id':move_line.product_id.uom_id.id,
                                    'package_id':move_line.result_package_id.id,
                                    'lot_id':move_line.lot_id.id,
                                    'lot_name':move_line.lot_id.name,
                                    'qty_done':move_line.qty_done,
                                    'location_id':self.location_id.id,
                                    'location_dest_id':self.location_dest_id.id
                                }

                                self.move_line_ids_without_package = [(0,0,new_move_line)]

                                move_line.z_done = True

                    move_count+=1
                else:
                    # Different lot for the differnt products
                    for move_line in move.move_line_ids:
                        if move_line.state == 'done' and move_line.z_done == False :

                            current_move = self.env['stock.move'].search([('picking_id','=',self.id),('product_id','=',move_line.product_id.id)])
                            new_move_line = {
                                'move_id':current_move.id,
                                'product_id':move_line.product_id.id,

                                'product_uom_id':move_line.product_id.uom_id.id,
                                'package_id':move_line.result_package_id.id,
                                'lot_id':move_line.lot_id.id,
                                'lot_name':move_line.lot_id.name,
                                'qty_done':move_line.qty_done,
                                'location_id':self.location_id.id,
                                'location_dest_id':self.location_dest_id.id
                            }

                            self.move_line_ids_without_package = [(0,0,new_move_line)]
                            move_count += 1
                            move_line.z_done = True


    # Restic the user warehouse wise based on the User acess
    def button_validate(self):
        # self.button_check()
        if self.env.user.sto_warehouse_line.from_warehouse_id:
            if self.picking_type_id.warehouse_id.id != self.env.user.sto_warehouse_line.from_warehouse_id.id:
                raise UserError(_('You are not authorised person for warehouse: %s.')% self.picking_type_id.warehouse_id.name)

            return super(Picking,self).button_validate()
        
        else:
            return super(Picking,self).button_validate()






    # def fetch_detailed_operation(self):

    #     picking = self.env['stock.picking'].search([
    #         ('inter_company_transfer_id','=',self.inter_company_transfer_id.id),
    #         ('op_code','=','outgoing'),('z_qty_count','=',False)])
    #     if picking:
    #         for move_line in self.move_line_ids_without_package:
    #             if move_line.state == 'done' :
    #                 self.move_line_ids_without_package = [(2,move_line.id)]
    #         for move in picking.move_ids_without_package:
    #             move_count = 0
    #             for move_line in move.move_line_ids:

    #                 # if move_line.state == 'done' :
    #                 new_move_line = {
    #                     'move_id':self.move_ids_without_package[move_count].id,
    #                     'product_id':move_line.product_id.id,
    #                     'product_uom_id':move_line.product_uom_id.id,
    #                     'package_id':move_line.result_package_id.id,
    #                     'lot_id':move_line.lot_id.id,
    #                     'lot_name':move_line.lot_id.name,
    #                     'qty_done':move_line.qty_done,
    #                     'location_id':self.location_id.id,
    #                     'location_dest_id':self.location_dest_id.id
    #                 }
    #                 self.move_line_ids_without_package = [(0,0,new_move_line)]
    #                 # move_line.z_done = True
    #                 move_count += 1