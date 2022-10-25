from odoo.tools.float_utils import float_is_zero, float_compare
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import Warning
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp
import datetime
from datetime import datetime


class IndentOrder(models.Model):
    _name= 'indent.order'
    _description = 'Indent Order wizard'

    # @api.onchange('picking_type_id')
    # def onchange_opr_type(self):
    #     for rec in self:
    #         return {'domain':{'location_id':[('picking_type_id','=',rec.picking_type_id.code)]}}

    
    product_lines =fields.One2many('indent.order.line', 'mrp_indent_product_line_id', string='Order Lines')

    move_lines = fields.One2many('stock.move', 'mrp_indent_stock_line_id', string='Moves', copy=False, readonly=True)
    name = fields.Char(string='Name', readonly=True, copy=False)
    state = fields.Selection(
            [('draft', 'Draft'),
             ('waiting_approval', 'Waiting for Approval'),
             ('inprogress', 'Ready to Transfer'),
             ('done', 'Done'),
             ('cancel', 'Cancel'),
             ('reject', 'Rejected')], string='State', readonly=True, default='draft', track_visibility='onchange')
    item_for = fields.Selection([('mrp', 'Produce'), ('other', 'Other')], string='Order for', default='other',
                                readonly=True)

    requirement_id = fields.Selection([('1', 'Ordinary'), ('2', 'Urgent')],readonly=True, default='1')
    # origin = fields.Many2one('mrp.production', string='Source Document', copy=False)
    issued_by = fields.Char(string='Issued By')
    # z_analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account')
    indent_date = fields.Datetime(string='Material Requisition Date' ,default=fields.Datetime.now,readonly=True)
    require_date = fields.Datetime(string='Required Date', default=fields.Datetime.now,readonly=True)
    approve_date = fields.Datetime(string='Approve Date', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    date_order = fields.Datetime(string='Order Date')
    company_id = fields.Many2one('res.company', string='Company')
    picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type',required=True, domain="[('code','=','internal')]")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
    procurement_group_id = fields.Char("Group id")
    picking_ids = fields.Many2many('stock.picking', string='Receptions', copy=False, store=True)
    location_id = fields.Many2one('stock.location', string='Source Location')
    location_dest_id = fields.Many2one('stock.location', string='Destination Location',required=True)
    status = fields.Char(string="Status")
    status1 = fields.Char(string="Status")

   
    def indent_transfer_move_confirm_new(self):
        StockPicking = self.env['stock.picking']
        for order in self:
            if any([order.product_lines.mapped('product_id.type')]):
                res = order._prepare_pickings()
                picking = StockPicking.create(res)
                moves = order.product_lines._create_stock_moves(picking)
                self.status = 'Converted'
        self.write({'state': 'done'})
        return True

   
    def indent_check_new(self):
        indent_count = self.env['indent.order']
        if not indent_count:
            vals = {
                # 'origin': self.origin.id,
                'company_id': self.company_id.id,
                'picking_type_id': self.picking_type_id.id,
                'location_dest_id': self.location_dest_id.id,

            }
            indent_obj = self.env['indent.order'].create(vals)
            move_lines_obj = self.env['indent.order.line']
            for line in self.product_lines:
                if line.sequence == True:
                    line.update({
                        'mrp_indent_product_line_id': indent_obj.id,
                        'sequence':False,
                    })  
                
    
    
    def indent_cancel(self):
        self.write({'state': 'cancel'})
        return True

    
    def indent_reject(self):
        self.write({'state': 'reject'})
        return True


    @api.model
    def _prepare_pickings(self):
        return {
            'picking_type_id': self.picking_type_id.id,
            'name':self.name,
            'partner_id': self.partner_id.id,
            'date': self.date_order,
            # 'origin': self.name,
            'location_dest_id': self.location_dest_id.id,
            #'analytic_account_id': self.z_analytic_account_id.id,
            'location_id': self.location_id.id,
            'company_id': self.company_id.id,
        }


    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('indent.order')
        return super(IndentOrder, self).create(vals)

    
    # def button_indent_confirm(self):
    #     for indent in self:
    #         if indent.item_for == 'mrp':
    #             if not indent.move_lines:
    #                 raise exceptions.Warning(_("Warning "
    #                                            "You cannot confirm an Material Requisition %s which has no line." % indent.name))
    #             else:
    #                 indent.write({'state': 'waiting_approval'})
    #                 indent.origin.write({'indent_state': 'waiting_approval'})
    #         else:
    #             if not indent.product_lines:
    #                 raise exceptions.Warning(_("Warning "
    #                                            "You cannot confirm an Material Requisition %s which has "
    #                                            "no product line." % indent.name))
    #             else:
    #                 indent.write({'state': 'waiting_approval'})


   
    def button_indent_confirm_approve(self):
        todo = []
        for o in self:
            if not any(line for line in o.product_lines):
                raise exceptions.Warning(_('Error!'),
                              _('You cannot Approve a order without any order line.'))

            for line in o.product_lines:
                if line:
                    todo.append(line.id)

        appr_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.env['indent.order.line'].action_confirm(todo)

        for id in self.ids:
            self.write({'state': 'inprogress', 'approve_date': appr_date})
        return True

    
    def button_indent_transfer(self):
        name = self.name
        move_lines_obj = self.env['stock.move']
        if self.product_lines:
            for line in self.product_lines:
                if line.product_id.type != 'service':
                    if line.location_id:
                        if line.location_dest_id:
                            tot_qty = 0
                            obj_quant = self.env['stock.quant'].search([('product_id', '=', line.product_id.id),
                                                                        ('location_id', '=', line.location_id.id)])
                            for obj in obj_quant:
                                tot_qty += obj.quantity
                            move_line = {}
                            if line.product_id.type == 'consu':
                                move_line = {
                                    'product_id': line.product_id.id,
                                    'product_uom_qty': line.product_uom_qty,
                                    'product_uom': line.product_id.uom_id.id,
                                    'name': line.product_id.name,
                                    'location_id': line.location_id.id,
                                    'location_dest_id': line.location_dest_id.id,
                                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    'date_expected': self.require_date,
                                    'invoice_state': "none",
                                    # 'origin': name,
                                    'mrp_indent_stock_line_id': self.id
                                }
                                move_lines_obj.create(move_line)
                            else:
                                move_line = {}
                                if tot_qty >= line.product_uom_qty:
                                    move_line = {
                                                'product_id': line.product_id.id,
                                         
                                                'product_uom_qty': line.product_uom_qty,
                                                'product_uom': line.product_id.uom_id.id,
                                                'name': line.product_id.name,
                                                'location_id': line.location_id.id,
                                                'location_dest_id': line.location_dest_id.id,
                                                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                'date_expected': self.require_date,
                                                'invoice_state': "none",
                                                # 'origin': name,
                                                'mrp_indent_stock_line_id': self.id
                                                }
                                    move_lines_obj.create(move_line)
                                else:
                                    if tot_qty:
                                        raise exceptions.Warning((" No sufficient stock for product ' %s ' in '%s'.  "
                                                                  "Available quantity is %s %s.") %
                                                                 (line.product_id.name, line.location_id.name, tot_qty,
                                                                  line.product_uom_qty))
                                    else:
                                        raise exceptions.Warning(
                                                      (" No stock for product ' %s ' in '%s'."
                                                       "  Please continue with another location ") % (line.product_id.name,
                                                                                                      line.location_id.name))
                        else:
                            raise exceptions.Warning((" Destination Location is not set properly for' %s '. "
                                                      "So Please cancel this Material Requisition and create a new one please.")
                                                     % line.product_id.name)
                    else:
                        raise exceptions.Warning(("Source Location is not set properly for ' %s '.  "
                                                  "Please go and set Source Location.")
                                                 % line.product_id.name)
                else:
                    raise exceptions.Warning("This product is a service type product.")
        else:
            raise exceptions.Warning('You cannot Transfer a order without any product line.')
        self.write({'state': 'move_created'})

    

class IndentOrderLine(models.Model):
    _name = 'indent.order.line'
    _description = 'Indent Order Line wizard'

    
    def action_confirm(self, todo):
        self.write({'state': 'inprogress'})
        return True

    mrp_indent_product_line_id = fields.Many2one('indent.order')
    
    sequence = fields.Boolean(string='Create Material Requisition', default=False)
    product_id = fields.Many2one('product.product', string='Product')
    product_uom_qty = fields.Float(string='Initial Demand')
    product_uom_qty_reserved = fields.Float(string='Reserved')
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure')
    location_id = fields.Many2one('stock.location', string='Source Location',related="mrp_indent_product_line_id.location_id")
    location_dest_id = fields.Many2one('stock.location', string='Destination Location',related="mrp_indent_product_line_id.location_dest_id")
    move_ids = fields.One2many('stock.move', 'indent_line_id', string='Reservation', readonly=True, ondelete='set null', copy=False)
    

    state = fields.Selection(
            [('draft', 'Draft'),
             ('waiting_approval', 'Waiting for Approval'),
             ('inprogress', 'Ready to Transfer'),
             ('done', 'Done'),
             ('cancel', 'Cancel'),
             ('reject', 'Rejected')], string='State', default='draft', related='mrp_indent_product_line_id.state')
    


    
        

        
    def _create_stock_moves(self, picking):
        moves = self.env['stock.move']
        done = self.env['stock.move'].browse()
        for line in self:
            for val in line._prepare_stock_moves(picking):
                done += moves.create(val)
        return done

    
    def _prepare_stock_moves(self, picking):
        """ Prepare the stock moves data for one order line. This function returns a list of
        dictionary ready to be used in stock.move's create()
        """
        self.ensure_one()
        res = []
        if self.product_id.type not in ['product', 'consu']:
            return res
        qty = 0.0
        for move in self.move_ids:
            qty += move.product_uom_qty
        template = {
            'name': self.product_id.name,
            'product_id': self.product_id.id,
            'product_uom': self.product_id.uom_id.id,
            'location_id': self.mrp_indent_product_line_id.location_id.id,
            'location_dest_id': self.mrp_indent_product_line_id.location_dest_id.id,
            'picking_id': picking.id,
            'state': 'draft',
            'indent_line_id': self.id,
            'company_id': self.mrp_indent_product_line_id.company_id.id,
            'picking_type_id': self.mrp_indent_product_line_id.picking_type_id.id,
            # 'origin': self.mrp_indent_product_line_id.name,
   
        }
        diff_quantity = self.product_uom_qty - qty
        # if float_compare(diff_quantity, 0.0,  precision_rounding=self.product_uom.rounding) >= 0:
        template['product_uom_qty'] = diff_quantity
        res.append(template)
        return res

