import logging
from psycopg2 import sql, extras
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo.tools.translate import _
from odoo.tools import email_re, email_split
from odoo.exceptions import UserError, AccessError
from odoo.addons.phone_validation.tools import phone_validation
from collections import OrderedDict
import pdb

class StockPicking(models.Model):
    _inherit = 'stock.picking'


    bill_number = fields.Char()
    bill_date = fields.Date()
    bill_value = fields.Integer()
    payment_status = fields.Selection([('invoice_booked', 'Invoice Booked'), ('invoice_processed', 'invoice Processed'), ('payment_done', 'Payment Done')])
    payment_date = fields.Date()
    payment_reference = fields.Char()
    payment_value = fields.Float()
    grn_value = fields.Float(compute="get_grn_value", store=True)
    from_po = fields.Boolean(compute="get_grn_value", store=True)
    picking_type_name = fields.Char(related="picking_type_id.name", store=True, string="picking type name")


    @api.depends('state','move_ids_without_package')
    def get_grn_value(self):
        for l in self:
            tot_grn_val = 0.0
            if l.state == 'done':
                for each_line in l.move_ids_without_package:
                    tax_p= 0.0
                    if each_line.purchase_line_id:
                        tax_p = each_line.purchase_line_id.price_tax/each_line.purchase_line_id.product_qty
                    tot_grn_val += ((each_line.price_unit * each_line.quantity_done) + (tax_p *each_line.quantity_done))

                l.grn_value = tot_grn_val

            else:
                for each_line in l.move_ids_without_package:
                    if each_line.purchase_line_id:
                        l.from_po = True
                l.grn_value = tot_grn_val



class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    contact_person_id = fields.Many2one('res.partner')



