# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import api, fields, models, SUPERUSER_ID, _

class StockMove(models.Model):
    _inherit = 'stock.move'

    def print_all_barcodes_wiz(self):
        return self.env.ref('odoov13_21.curefit_barcode_print_pdf_stock_move').report_action(self)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def print_all_barcodes_con(self):
        return self.env.ref('odoov13_21.curefit_barcode_print_pdf_stock_picking').report_action(self)

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    def print_barcode(self):
        return self.env.ref('odoov13_21.curefit_barcode_print_pdf_stock_move_line').report_action(self)