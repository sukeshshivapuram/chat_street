from odoo import models, api, fields,_
from odoo.exceptions import AccessError, UserError, ValidationError
import pdb

class PricelistsCity(models.Model):
    _name = "pricelist.city"

    # responsible_id = fields.Many2one( "res.users",string='Resposible')
    name = fields.Char("City Name")

class Warehouse(models.Model):
    _inherit = "stock.warehouse"



    city_id = fields.Many2one('pricelist.city',"City")

    

class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"



    city_id = fields.Many2one('pricelist.city' ,"City")


class purchaseorder(models.Model):
    _inherit = "purchase.order"

    product_ids = fields.Many2many('product.product',compute='get_products')

    @api.depends('partner_id','picking_type_id')
    def get_products(self):
        for rec in self:
            if rec.partner_id and rec.picking_type_id:
                query = """SELECT id FROM product_product WHERE product_tmpl_id IN
                            (SELECT product_tmpl_id FROM product_supplierinfo WHERE
                                name = %s AND city_id = %s)
                            """%(rec.partner_id.id,
                                rec.picking_type_id.warehouse_id.city_id.id)
                self.env.cr.execute(query)
                products = [product[0] for product in self.env.cr.fetchall()]
                rec.product_ids = [(6, 0, products)]
            else:
                rec.product_ids = False

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.constrains('product_id','b_name')
    def check_name(self):
        for rec in self:
            brand_obj=self.env['product.brand.lines']
            b_names= [x.name for x in brand_obj.search([])]
            b_names.append(False)
            if rec.b_name not in b_names:
                raise ValidationError(_(""" No Matching records found for the Brand %s
                                        """%(rec.b_name)))
            if rec.product_id.id not in rec.order_id.product_ids.ids:
                raise ValidationError(_("""%s does not have a pricelist for %s at %s
                                        """%(rec.order_id.partner_id.name,
                                            rec.product_id.name,
                                            rec.order_id.picking_type_id.warehouse_id.city_id.name)))