from odoo import api, fields, models, SUPERUSER_ID, _

class PrintBarcodes(models.Model):
    _name = 'print.barcodes'

    name = fields.Char(related='sequence_id.name')
    sequence_id = fields.Many2one('ir.sequence')
    number_of_barcodes_to_generate = fields.Integer()

    def barcode_list(self):
        barcodes = []
        for num in range(self.number_of_barcodes_to_generate):
            barcodes.append(self.env['ir.sequence'].next_by_code(self.sequence_id.code))
        return barcodes

    def generate_print(self):
        if self.sequence_id and self.number_of_barcodes_to_generate:
            return self.env.ref('barcode_generator.print_generated_barcodes').report_action(self)