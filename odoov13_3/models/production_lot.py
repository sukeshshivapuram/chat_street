# -*- coding: utf-8 -*-

import datetime
from odoo.exceptions import ValidationError
from datetime import timedelta
from odoo import api, fields, models, SUPERUSER_ID, _



class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    manufacture_date = fields.Datetime(string="Date of Manufacture",required=True)

    @api.onchange('manufacture_date','product_id')
    def _fetch_dates(self):
        if self.manufacture_date and self.product_id:
            if self.product_id.use_time:
                self.use_date = self.manufacture_date + timedelta(days=self.product_id.use_time)
            if self.product_id.life_time:
                self.life_date = self.manufacture_date + timedelta(days=self.product_id.life_time)
            if self.product_id.removal_time:
                self.removal_date = self.manufacture_date + timedelta(days=self.product_id.removal_time)
            if self.product_id.alert_time:
                self.alert_date = self.manufacture_date + timedelta(days=self.product_id.alert_time)

    @api.onchange('use_date','life_date','removal_date','alert_date')
    def _validate_dates(self):
        if self.manufacture_date and self.alert_date and not self.manufacture_date < self.alert_date:
            raise ValidationError(_('Alert Date Must Be After Manufacture Date'))
        if self.alert_date and self.removal_date and not self.alert_date < self.removal_date:
            raise ValidationError(_('Removal Date Must Be After Alert Date'))
        if self.removal_date and self.use_date and not self.removal_date < self.use_date:
            raise ValidationError(_('Use Date Must Be After Removal Date'))
        if self.use_date and self.life_date and not self.use_date < self.life_date:
            raise ValidationError(_('Life Date Must Be After Removal Date'))
        if self.life_date and self.life_date <= datetime.datetime.now():
            raise ValidationError(_('Product Has Passed Expiration Date'))
        if not self.manufacture_date:
            self.use_date = self.removal_date = self.alert_date = self.life_date = False