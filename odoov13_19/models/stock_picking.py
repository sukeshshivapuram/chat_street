"""
For inter_company_transfer_ept module.
"""
from odoo import fields, api, models


class Picking(models.Model):
    """
    Inherited for adding relation with inter company transfer.
    @author: Maulik Barad on Date 25-Sep-2019.
    """
    _inherit = 'stock.picking'

    inter_company_transfer_id = fields.Many2one('inter.company.transfer.ept', string="ICT",
                                                copy=False, help="Reference of ICT.")
    op_code = fields.Selection([
        ('incoming','1'),
        ('outgoing','2'),
        ('internal','3')],related='picking_type_id.code')

    def _create_backorder(self):
        """
        Inherited for adding ICT relation to backorder also.
        @author: Maulik Barad on Date 09-Oct-2019.
        """
        res = super(Picking, self)._create_backorder()
        for backorder in res:
            if backorder.backorder_id and backorder.backorder_id.inter_company_transfer_id:
                backorder.write({"inter_company_transfer_id":backorder.backorder_id.\
                                 inter_company_transfer_id.id})
        return res

    def fetch_detailed_operation(self):

        picking = self.env['stock.picking'].search([
            ('inter_company_transfer_id','=',self.inter_company_transfer_id.id),
            ('op_code','=','outgoing')])
        if picking:
            for move_line in self.move_line_ids_without_package:
                self.move_line_ids_without_package = [(2,move_line.id)]
            for move_line in picking.move_line_ids_without_package:
                new_move_line = {}
                new_move_line['product_id'] = move_line.product_id.id
                new_move_line['product_uom_id'] = move_line.product_uom_id.id
                new_move_line['package_id'] = move_line.result_package_id.id
                new_move_line['lot_id'] = move_line.lot_id.id
                new_move_line['lot_name'] = move_line.lot_id.name
                new_move_line['qty_done'] = move_line.qty_done
                new_move_line['location_id'] = self.location_id.id
                new_move_line['location_dest_id'] = self.location_dest_id.id
                self.move_line_ids_without_package = [(0,0,new_move_line)]