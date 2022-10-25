# -*- coding: utf-8 -*-

import logging
from odoo import models,_
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class StockIndentState(models.TransientModel):
    _name = 'stock.indent.order.state'
    _description = "Wizard - stock.indent.order.state"


    def get_current_id(self):
        indents = self._context.get('active_ids')
        for each_po in indents:
            indent_ids = self.env['stock.indent.order'].browse(indents).\
                filtered(lambda x: x.state == 'draft' )
            if indent_ids:
                for indent in indent_ids:
                    if indent.product_lines and indent.location_id and indent.location_dest_id:
                        indent.indent_transfer_move_confirm_new()
                    else:
                        raise ValidationError(_("Fill the locations and the Products for the indent ref %s.")%indent.name)

    




