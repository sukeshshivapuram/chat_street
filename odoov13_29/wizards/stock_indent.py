# -*- coding: utf-8 -*-

import logging
from odoo import models,_
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class StockTranferState(models.TransientModel):
    _name = 'stock.tranfer.order.state'
    _description = "Wizard - stock.indent.order.state"


    def get_current_ids(self):
        tranfers = self._context.get('active_ids')
        for each_sto in tranfers:
            tranfer_ids = self.env['inter.company.transfer.ept'].browse(each_sto).\
                filtered(lambda x: x.state == 'draft' )
            if tranfer_ids:
                for tranfe in tranfer_ids:
                    if tranfe.inter_company_transfer_line_ids and tranfe.source_warehouse_id and tranfe.destination_warehouse_id:
                        tranfe.process_ict()
                    else:
                        raise ValidationError(_("Fill the Warehouse and the Products for the indent ref %s.")%tranfe.name)

    




