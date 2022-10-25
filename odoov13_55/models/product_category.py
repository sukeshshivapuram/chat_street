from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import config, float_compare

class ProductCategory(models.Model):
    _inherit = "product.category"

    z_description = fields.Char('Description')
    z_release = fields.Boolean('Release')


    allow_negative_stock = fields.Boolean(
        string='Allow Negative Stock',
        help="Allow negative stock levels for the stockable products "
        "attached to this category. The options doesn't apply to products "
        "attached to sub-categories of this category.")

class ProductTemplate(models.Model):
    _inherit = "product.template"

    categ_id = fields.Many2one(
        'product.category', 'Product Category',
        change_default=True,required=True,domain=[('z_release', '=', 'True')])

    allow_negative_stock = fields.Boolean(
        string='Allow Negative Stock',
        help="If this option is not active on this product nor on its "
        "product category and that this product is a stockable product, "
        "then the validation of the related stock moves will be blocked if "
        "the stock level becomes negative with the stock move.")
    item_category = fields.Many2one('item.category', string = 'Item Category')
    product_group_primary = fields.Many2one('product.group.primary', domain="[('item_category', '=', item_category)]", string = 'Product Group Primary')
    product_group_secondary = fields.Many2one('product.group.secondary', domain="[('product_group_primary', '=', product_group_primary)]", string = 'Product Group Secondary')


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    # @api.multi
    @api.constrains('product_id', 'quantity')
    def check_negative_qty(self):
        p = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        check_negative_qty = (
            (config['test_enable'] and
             self.env.context.get('test_stock_no_negative')) or
            not config['test_enable']
        )
        if not check_negative_qty:
            return
        for quant in self:
            if (
                float_compare(quant.quantity, 0, precision_digits=p) == -1 and
                quant.product_id.type == 'product' and
                not quant.product_id.allow_negative_stock and
                not quant.product_id.categ_id.allow_negative_stock and
                quant.location_id.usage in ['internal', 'transit']
            ):
                msg_add = ''
                if quant.lot_id:
                    msg_add = _(" lot '%s'") % quant.lot_id.name_get()[0][1]
                raise ValidationError(_(
                    "You cannot validate this stock operation because the "
                    "stock level of the product '%s'%s would become negative "
                    "(%s) on the stock location '%s' and negative stock is "
                    "not allowed for this product.") % (
                        quant.product_id.name, msg_add, quant.quantity,
                        quant.location_id.complete_name))
