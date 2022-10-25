from odoo import models, api, fields,_


class SaleOrder(models.Model):
    _inherit = "sale.order"

    responsible_id = fields.Many2one( "res.users",string='Resposible')
    
    # ('warehouse_user', 'in', self.env.user.ids)

class StockPicking(models.Model):
    _inherit = "stock.picking"

    user_id = fields.Many2one('res.users', 'Responsible', tracking=True,
        domain=lambda self: [('groups_id', 'in', self.env.ref('stock.group_stock_user').id),
        ('groups_id', 'in', self.env.ref('odoov13_7.group_stock_user_reposible').id), 
        ('warehouse_user' ,'in', self.domain_user_id.ids)], 

        states={'done': [('readonly', True)], 'cancel': [('readonly', True)], 'draft': [('readonly', False)],'draft': [('readonly', False)],
        		'assigned': [('readonly', False)],'confirmed': [('readonly', False)],'waiting': [('readonly', False)]},
        store=True,compute='_compute_user')
    domain_user_id = fields.Many2one( "stock.warehouse",string='Domain',compute='get_warehouse_id',store=True)

    @api.depends('picking_type_id')
    def get_warehouse_id(self):
        for l in self:
            if l.picking_type_id.warehouse_id:
                l.domain_user_id = l.picking_type_id.warehouse_id.id

    @api.depends('sale_id')
    def _compute_user(self):
        for l in self:
            ordr_id = self.env['sale.order'].search([('id','=',l.sale_id.id)])
            for line in ordr_id:
                l.user_id = line.responsible_id.id

class WarehouseUser(models.Model):
    _inherit='res.users'
    warehouse_user = fields.Many2one("stock.warehouse", string="Warehouse")

    