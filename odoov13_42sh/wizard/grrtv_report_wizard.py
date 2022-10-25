# -*- coding: utf-8 -*-

import io
import json

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import date_utils


class GRRTVReportWizard(models.TransientModel):
    _name = 'grrtv.report.wizard'
    _description = 'GRRTV Report Wizard'

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True, default=fields.Date.today)
    excel_file = fields.Binary(string='Download Report Excel')

    def action_grrtv_report(self):
        if self.date_from > self.date_to:
            raise ValidationError(_('Date From should not be greater than Date To.'))
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
        }
        return {
            'type': 'ir_actions_xlsx_download',
            'data': {
                'model': 'grrtv.report.wizard',
                'options': json.dumps(data, default=date_utils.json_default),
                'output_format': 'xlsx',
                'report_name': 'GRRTV Report',
            }
        }

    def get_xlsx_report(self, data, response):
        StockMove = self.env['stock.move']
        StockWarehouse = self.env['stock.warehouse']
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        moves = StockMove.search([('date', '>=', date_from), ('date', '<=', date_to), ('state', '=', 'done')])
        warehouses = StockWarehouse.search([('company_id', '=', self.env.company.id)])
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        head = workbook.add_format({'align': 'center', 'bold': True})
        sheet.write(0, 0, 'Item Name', head)
        sheet.write(0, 1, 'Item Category Name', head)
        sheet.write(0, 2, 'Unit', head)
        sheet.write(0, 3, 'Rate', head)
        sheet.write(0, 4, 'Item ID', head)
        col = 5
        ascci_code = 69
        for warehouse in warehouses:
            sheet.write(0, col, warehouse.name, head)
            ascci_code += 1
            col += 1

        sheet.write(0, col, 'Total Qty', head)
        sheet.write(0, col + 1, 'Total Amount', head)

        srow = 1
        last_col = 0
        products = []
        products1 = []
        for move in moves.filtered(lambda move: move.picking_type_id.is_rtv):
            location_id = move.picking_id.location_id
            # location_id = move.picking_id.location_id if move.picking_id.picking_type_code == 'outgoing' else move.picking_id.location_dest_id
            location = location_id.complete_name
            warehouse_code = ''
            if '/' in location:
                warehouse_code = location.split('/')[0]
            else:
                warehouse_code = location
            unique = False
            if move.product_id.id not in products1:
                products1.append(move.product_id.id)
                unique = True
                r = srow
            else:
                unique = False
            if move.product_id.id not in [p.get('product_id_' + warehouse_code) for p in products]:
                products.append({'product_id_' + warehouse_code: move.product_id.id, 'row': r, 'col': 0, 'val': 0})
            if unique:
                sheet.write(srow, 0, move.product_id.name)
                sheet.write(srow, 1, move.product_id.categ_id.name)
                sheet.write(srow, 2, move.product_uom.name)
                sheet.write(srow, 3, move.product_id.standard_price)
                sheet.write(srow, 4, move.product_id.default_code)
            scol = 5
            total = 0
            grand_total_qty = 0
            grand_total_amount = 0
            for warehouse in warehouses:
                if warehouse.code == warehouse_code:
                    total = sum(move.move_line_ids.mapped('qty_done'))
                    for product in products:
                        if product.get('product_id_' + warehouse_code) == move.product_id.id:
                            val = product.get('val', 0)
                            product.update({'col': scol, 'val': val + total})
                    grand_total_qty += total
                else:
                    if unique:
                        sheet.write(srow, scol, 0)
                scol += 1
                last_col = scol
            if unique:
                srow += 1
        Product = self.env['product.product']
        rows = []
        for p in products:
            rows.append(str(p.get('row', 0) + 1))
            for warehouse in warehouses:
                product_id = p.get('product_id_' + warehouse.code)
                product = Product.browse(product_id)
                r = p.get('row', 1)
                c = p.get('col', 1)
                val = p.get('val', 0)
                sheet.write(r, c, val)
        for row in set(rows):
            formula = '=SUM(F' + row + ':' + chr(ascci_code) + row + ')'
            formula2 = '=(D' + row + '*' + chr(ascci_code + 1) + row + ')'
            for_col = chr(ascci_code + 1) + row
            for_col2 = chr(ascci_code + 2) + row
            sheet.write_formula(for_col, formula)
            sheet.write_formula(for_col2, formula2)
        # sheet.write(row, last_col + 1, product.standard_price * tot)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()