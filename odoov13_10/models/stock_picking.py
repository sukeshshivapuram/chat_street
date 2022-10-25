from odoo import models, fields, api
from datetime import date

class DraftReset(models.Model):
    _inherit = 'stock.picking'
    _description = 'Pack Print'

    
    # @api.multi
    def cf_pack_print_button(self):
        return self.env.ref('stock.report_package_barcode') .report_action(self)


    def get_package_group(self):
        list1 = []
        for lines in self.move_line_ids_without_package:
            list1.append(lines.result_package_id)
        package_group = list(set(list1))

        print('**************************', package_group)
        return package_group