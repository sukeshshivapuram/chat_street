# -*- coding: utf-8 -*-

import logging
from odoo import models,_
from odoo.exceptions import UserError
from datetime import datetime
import pdb

_logger = logging.getLogger(__name__)

class grn_unreserve(models.TransientModel):
    _name = 'grn.un.reserve'
    _description = "Wizard - grn.un.reserve"



    def get_price(self):
        """filter the records of the state 'draft' ,
        and will confirm this and others will be skipped"""

        quotations = self._context.get('active_ids')
        quotations_ids = self.env['stock.picking'].browse(quotations)
        quotations_ids.do_unreserve()
       



