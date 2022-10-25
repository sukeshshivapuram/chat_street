from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import ValidationError,UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime, timedelta
import pdb
class Brand(models.Model):
    _name = 'brand.brand'

    name = fields.Char()


class ProductBrandLines(models.Model):
    _name = 'product.brand.lines'

    product_tmpl_id = fields.Many2one('product.template')
    brand = fields.Many2one('brand.brand')
    pack_size = fields.Many2one('uom.uom')
    sku = fields.Char(string="SKU")
    name = fields.Char(compute = '_gen_name',store=True)

    @api.depends('brand','pack_size')
    def _gen_name(self):
        for rec in self:
            try:
                rec.name = rec.brand.name+' ['+rec.pack_size.name+']'
            except:
                rec.name = ''


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_brand_ids = fields.One2many('product.brand.lines','product_tmpl_id')
    brands = fields.Boolean()
    uom_cat_id = fields.Many2one('uom.category',related='uom_id.category_id')


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    warehouse_id = fields.Many2one('stock.warehouse')
    product_brand_id = fields.Many2one('product.brand.lines')



class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    del_to = fields.Many2one('stock.picking.type')
    product_brand_ids = fields.Many2many('product.brand.lines',compute='get_product_lines')

    @api.depends('partner_id','picking_type_id')
    def get_product_lines(self):
        for rec in self:
            price_lists = self.env['product.supplierinfo'].search([
                ('name','=',rec.partner_id.id),
                ('city_id','=',rec.picking_type_id.warehouse_id.city_id.id)])
            brands = []
            for price_list in price_lists:
                if price_list.product_brand_id:
                    brands.append(price_list.product_brand_id.id)
            rec.product_brand_ids = [(6, 0, brands)]

    @api.onchange('del_to')
    def copy_vals(self):
        self.picking_type_id = self.del_to


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_brand_id = fields.Many2one('product.brand.lines')
    product_tmpl_id = fields.Many2one('product.template')
    b_name = fields.Char("Brand Name",store=True)


    product_brand_id_helper = fields.Many2one('product.brand.lines' ,compute='get_brand',store=True)

    

    @api.depends('b_name')
    def get_brand(self):
        for l in self:
            if l.b_name :
                b_id =self.env['product.brand.lines'].search([('product_tmpl_id','=',l.product_id.product_tmpl_id.id),('name','=', l.b_name)])
                l.product_brand_id_helper = b_id.id
                l.product_brand_id = b_id.id
            else:
                l.product_brand_id_helper = False
    

    @api.onchange('product_id')
    def set_template(self):
        self.product_tmpl_id = self.product_id.product_tmpl_id

    

    @api.onchange('product_qty', 'product_uom', 'product_brand_id')
    def _onchange_quantity(self):
        
        if not self.product_id:
            return
        params = {'order_id': self.order_id}
        seller = self.product_id._select_seller(
            partner_id=self.partner_id,
            quantity=self.product_qty,
            date=self.order_id.date_order and self.order_id.date_order.date(),
            uom_id=self.product_uom,
            params=params)

        if seller or not self.date_planned:
            self.date_planned = self._get_date_planned(seller).strftime(DEFAULT_SERVER_DATETIME_FORMAT)

        if not seller:
            if self.product_id.seller_ids.filtered(lambda s: s.name.id == self.partner_id.id):
                self.price_unit = 0.0
            return

        price_unit = self.env['account.tax']._fix_tax_included_price_company(seller.price, self.product_id.supplier_taxes_id, self.taxes_id, self.company_id) if seller else 0.0
        if price_unit and seller and self.order_id.currency_id and seller.currency_id != self.order_id.currency_id:
            price_unit = seller.currency_id._convert(
                price_unit, self.order_id.currency_id, self.order_id.company_id, self.date_order or fields.Date.today())

        if seller and self.product_uom and seller.product_uom != self.product_uom:
            price_unit = seller.product_uom._compute_price(price_unit, self.product_uom)

        if self.product_brand_id:
            self.product_uom = self.product_brand_id.pack_size.id


            price_list =  self.env['product.supplierinfo'].search([
                ('name','=',self.order_id.partner_id.id),
                ('city_id','=',self.order_id.picking_type_id.warehouse_id.city_id.id),
                ('product_tmpl_id','=',self.product_id.product_tmpl_id.id),
                ('product_brand_id','=',self.product_brand_id.id)])

            if len(price_list.ids)>1:
                raise UserError(("For the product %s have the Multiple Price List ")%(self.product_id.name))
            price_unit = price_list.price

            self.date_planned = datetime.now() + timedelta(days=price_list.delay)
        if   self.product_id.brands== False:

            price_list = self.env['product.supplierinfo'].search([
                ('name','=',self.order_id.partner_id.id),
                ('product_tmpl_id','=',self.product_id.product_tmpl_id.id),
                ('city_id','=',self.order_id.picking_type_id.warehouse_id.city_id.id)])
            price_unit = price_list.price

            self.date_planned = datetime.now() + timedelta(days=price_list.delay)
        self.price_unit = price_unit





class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    product_brand_id = fields.Many2one('product.brand.lines')


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        for move in self.move_ids_without_package:
            for line in move.move_line_nosuggest_ids:
                line.lot_id.product_brand_id = line.move_id.purchase_line_id.product_brand_id.id
            if move.quantity_done == 0 and self.picking_type_id.validate_done_qty:
                raise ValidationError(_("You have not recorded done quantities yet"))
                # print('\n'*10,line.lot_id.name,' : ',line.move_id.purchase_line_id.product_brand_id.name,'\n'*10)

        return super(StockPicking,self).button_validate()

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    product_brand_id = fields.Many2one('product.brand.lines',related='lot_id.product_brand_id')