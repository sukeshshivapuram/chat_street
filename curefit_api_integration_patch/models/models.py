from odoo import api, fields, models, SUPERUSER_ID, _
import json
import requests

"""LOGGING"""
class CfApiAggLog(models.Model):
    _name = 'cf.api.agg.log'
    _description = 'Aggrigation API Call Logs'

    product_ref = fields.Char()
    warehouse_ref = fields.Char()
    product_id = fields.Many2one('product.product', compute="_get_product")
    quantity = fields.Float()
    uom_id = fields.Many2one('uom.uom',compute="_get_product")

    @api.depends('product_ref')
    def _get_product(self):
        for rec in self:
            rec.product_id = self.env['product.product'].search([('default_code','=',rec.product_ref)]).id
            rec.uom_id = rec.product_id.uom_id.id

class CfApiLiqLog(models.Model):
    _name = 'cf.api.liq.log'
    _description = 'Liquidation API Call Logs'

    transaction_ref = fields.Char()
    product_ref = fields.Char()
    product_id = fields.Many2one('product.product',compute="_get_product")
    warehouse_ref = fields.Char()
    req_qty = fields.Float()
    pre_liq_qty = fields.Float()
    act_qty = fields.Float()
    location_id = fields.Many2one('stock.location')
    picking_id = fields.Many2one('stock.picking')
    conf_count = fields.Integer()
    last_conf_time = fields.Datetime()
    assign_count = fields.Integer()
    last_assign_time = fields.Datetime()
    valid_count = fields.Integer()
    last_valid_time = fields.Datetime()
    unres_count = fields.Integer()
    last_unres_time = fields.Datetime()
    post_liq_qty = fields.Float()
    uom_id = fields.Many2one('uom.uom',compute="_get_product")

    @api.depends('product_ref')
    def _get_product(self):
        for rec in self:
            rec.product_id = self.env['product.product'].search([('default_code','=',rec.product_ref)]).id
            rec.uom_id = rec.product_id.uom_id.id
"""LOGGING"""

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = 'Warehouse Aggrigated inventory'

    cf_api_url = fields.Char("Server URL")
    cf_api_key = fields.Char("API Key")

    def set_values(self):
        super(ResConfigSettings,self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('curefit_api_integration_patch.cf_api_url',self.cf_api_url)
        self.env['ir.config_parameter'].sudo().set_param('curefit_api_integration_patch.cf_api_key',self.cf_api_key)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            cf_api_url = params.get_param('curefit_api_integration_patch.cf_api_url')
        )
        res.update(
            cf_api_key = params.get_param('curefit_api_integration_patch.cf_api_key')
        )
        return res


class AggregatedInventory(models.Model):
    _name = 'aggregated.inventory'

    warehouse_ref = fields.Char()
    product_ref = fields.Char()
    quantity = fields.Float()

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    warehouse_ref = fields.Char(compute='get_codes',store=True)
    product_ref = fields.Char(compute='get_codes',store=True)
    kitchen = fields.Boolean(compute='get_codes',store=True)
    aggregate_qty = fields.Float(compute='compute_aggregate',store=True)

    @api.depends('location_id', 'product_id')
    def get_codes(self):
        for rec in self:
            if rec.location_id.is_bin:
                rec.warehouse_ref = self.env['stock.warehouse'].search([('view_location_id','=',self.env['stock.location'].search([('id','=',int(rec.location_id.parent_path.split('/')[1]))]).id)]).code
            elif rec.location_id.is_kic:
                rec.warehouse_ref = rec.location_id.kc_ref
                rec.kitchen = True
            else:
                rec.warehouse_ref = False
            if rec.product_id.default_code:
                rec.product_ref = rec.product_id.default_code
            else:
                rec.product_ref = False

    @api.depends('warehouse_ref','product_ref','quantity','reserved_quantity')
    def compute_aggregate(self):
        
        API_ENDPOINT = self.env['ir.config_parameter'].sudo().get_param('curefit_api_integration_patch.cf_api_url')

        headers = {
            "Content-Type":"application/json",
            "x-api-key":self.env['ir.config_parameter'].sudo().get_param('curefit_api_integration_patch.cf_api_key')
        }

        prod_quant_list = []

        for rec in self:
            if rec.warehouse_ref and rec.product_ref:

                quants = self.env['stock.quant'].search([
                    ('warehouse_ref','=',rec.warehouse_ref),
                    ('product_ref','=',rec.product_ref)])
                
                quantity = 0
                
                for quant in quants:
                    quantity += quant.quantity - quant.reserved_quantity
                
                aggregate = self.env['aggregated.inventory'].search([
                    ('warehouse_ref','=',rec.warehouse_ref),
                    ('product_ref','=',rec.product_ref)])
                
                if aggregate:
                    aggregate.write({'quantity':quantity})
                
                else:
                    aggregate = self.env['aggregated.inventory'].create({
                        'warehouse_ref':rec.warehouse_ref,
                        'product_ref':rec.product_ref,
                        'quantity':quantity})
                
                rec.aggregate_qty = quantity

                prod_quant_list.append({
                    'product_ref': aggregate.product_ref,
                    'warehouse_ref': aggregate.warehouse_ref,
                    'quantity': aggregate.quantity
                    })

            else:
                rec.aggregate_qty = 0

        payload = {
            "inventoryUpdateRequest":prod_quant_list
        }
        """LOGGING"""
        for prod in prod_quant_list:
            self.env['cf.api.agg.log'].create({
                'product_ref': prod.get('product_ref'),
                'warehouse_ref': prod.get('warehouse_ref'),
                'quantity': prod.get('quantity')
            })
        """LOGGING"""
        if API_ENDPOINT and prod_quant_list:
            response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(payload))

    def liquid_cure(self,warehouse_ref,product_ref_qty,transaction_ref):

        """LOGGING"""
        loggs = []
        """LOGGING"""

        warehouse = self.env['stock.warehouse'].search([('code','=',warehouse_ref)])
        location = False
        if not warehouse:
            location = self.env['stock.location'].search([('is_kic','=',True),('kc_ref','=',warehouse_ref)])
            warehouse = self.env['stock.warehouse'].search([('view_location_id','=',self.env['stock.location'].search([('id','=',int(location.parent_path.split('/')[1]))]).id)])

        operation = self.env['stock.picking.type'].search([
            ('code','=','outgoing'),
            ('warehouse_id','=',warehouse.id)])

        msg = "Success"

        for product in product_ref_qty.keys():
            qty = self.env['aggregated.inventory'].search([('product_ref','=',product),('warehouse_ref','=',warehouse_ref)]).quantity
            """LOGGING"""
            logg = {
                'transaction_ref': transaction_ref,
                'product_ref': product,
                'warehouse_ref': warehouse_ref,
                'req_qty': product_ref_qty[product],
                'pre_liq_qty': qty,
                'conf_count': 0,
                'assign_count': 0,
                'valid_count': 0,
                'unres_count': 0
            }
            """LOGGING"""
            if qty < product_ref_qty[product]:
                product_ref_qty[product] = qty
                msg += "Insufficient_Stock of %s in %s - %s\n"%(product,warehouse_ref,qty)
                """LOGGING"""
                logg['act_qty'] = qty
            loggs.append(logg)
            """LOGGING"""

        # try:
        move = []
        for product in product_ref_qty.keys():
            if product_ref_qty[product]:
                pid = self.env['product.product'].search([('default_code','=',product)])
                move.append((0,0,{
                    'name' : '%s: [%s]%s'%(transaction_ref,product,pid.name),
                    'product_id' : pid.id,
                    'product_uom_qty' : product_ref_qty[product],
                    'product_uom' : pid.uom_id.id}))

        if len(move):
            picking = self.env['stock.picking'].create({
                'thru_api' : True,
                'origin' : transaction_ref,
                'picking_type_id' : operation.id,
                'location_id' : location.id if location else operation.default_location_src_id.id,
                'location_dest_id' : 5,
                'move_ids_without_package' : move
                })
            """LOGGING"""
            for logg in loggs:
                logg.update({
                    'location_id': location.id if location else operation.default_location_src_id.id,
                    'picking_id': picking.id
                })
            """LOGGING"""

            picking.action_confirm()
            """LOGGING"""
            for logg in loggs:
                logg['conf_count'] += 1
                logg['last_conf_time'] = fields.datetime.now()
            """LOGGING"""
            picking.action_assign()
            """LOGGING"""
            for logg in loggs:
                logg['assign_count'] += 1
                logg['last_assign_time'] = fields.datetime.now()
            """LOGGING"""
            for line in picking.move_line_ids_without_package:
                line.qty_done = line.product_uom_qty

            picking.button_validate()
            """LOGGING"""
            for logg in loggs:
                logg['valid_count'] += 1
                logg['last_valid_time'] = fields.datetime.now()
            """LOGGING"""
            while picking.state == 'assigned':
                picking.unreserve_qty()
                """LOGGING"""
                for logg in loggs:
                    logg['unres_count'] += 1
                    logg['last_unres_time'] = fields.datetime.now()
                """LOGGING"""
                picking.button_validate()
                """LOGGING"""
                for logg in loggs:
                    logg['valid_count'] += 1
                    logg['last_valid_time'] = fields.datetime.now()
            
            for logg in loggs:
                logg['post_liq_qty'] = self.env['aggregated.inventory'].search([('product_ref','=',product),('warehouse_ref','=',warehouse_ref)]).quantity
                self.env['cf.api.liq.log'].create(logg)
            """LOGGING"""
        # except:
        #     msg = "Unknown_Error"


        return msg


class Picking(models.Model):
    _inherit = 'stock.picking'

    thru_api = fields.Boolean()

    def action_generate_backorder_wizard(self):
        if self.thru_api:
            wiz = self.env['stock.backorder.confirmation'].create({'pick_ids': [(4, p.id) for p in self]})
            wiz._process(cancel_backorder=True)
            return
        else:
            return super(Picking,self).action_generate_backorder_wizard()