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


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    vendor_acceptence = fields.Selection([('accepted', 'Accepted'), ('rejected', 'Rejected')],string="Vendor Acceptance")
    rejected_reason = fields.Text('Reason')
    dispatch_status = fields.Selection([('dispatch', 'Dispatched')],string="Dispatch Status")
    dispatch_date = fields.Datetime()
    accepted_date = fields.Datetime()
    rejected_date = fields.Datetime()
    estimated_delivery_date = fields.Date()


    approve_delivery_date = fields.Selection([('accept','Accept'),('reject','Reject')], string="Approve Delivery Date")

