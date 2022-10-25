from odoo import api, fields, models, _





class StockQuant(models.Model):
    _inherit = 'stock.move'


    z_price = fields.Float(compute='compute_product_price',store=True)

    @api.depends('state','picking_id.state')
    def compute_product_price(self):
        for rec in self:
            if rec.state == 'done' and rec.picking_id.state == 'done':
                rec.z_price = rec.product_id.standard_price
            else:
                rec.z_price = False

            
