import base64
from collections import OrderedDict
from datetime import datetime

from odoo import http
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.tools import image_process
from odoo.tools.translate import _
from odoo.addons.portal.controllers.portal import pager as portal_pager, CustomerPortal
from odoo.addons.web.controllers.main import Binary
from werkzeug.wsgi import get_current_url

from odoo.addons.purchase.controllers.portal import CustomerPortal

class CustomerPortal(CustomerPortal):

	def _purchase_order_get_page_view_values(self, order, access_token, **kwargs):
	#
		def resize_to_48(b64source):
			if not b64source:
				b64source = base64.b64encode(Binary().placeholder())
			return image_process(b64source, size=(48, 48))

		receipts = request.env['stock.picking'].sudo().search([('origin', '=', order.name)])

		values = {
			'order_receipt':receipts,
		    'order': order,
		    'resize_to_48': resize_to_48,
		    'original_link': get_current_url(request.httprequest.environ),
		}
		return self._get_page_view_values(order, access_token, values, 'my_purchases_history', True, **kwargs)

	def update_vendor_inputs(self,  advantages, no_write=False, **kw):
		vendor_accept = advantages['vendor_acceptance_status']
		dispatch_info =  advantages['dispatch_status']
		rejected_reason = advantages['rejected_reasons']


		if kw.get('order_id'):
			order_id = kw.get('order_id')
			order = request.env['purchase.order'].sudo().search([('id', '=', order_id)])
			if vendor_accept:
			    order.write({'vendor_acceptence':vendor_accept['vendor_acceptence'],'estimated_delivery_date':vendor_accept['estimated_delivery_date']})
			    if order.vendor_acceptence == 'accepted' and order.accepted_date == False:
			    	order.write({'accepted_date':datetime.now()})
			    # elif order.vendor_acceptence == 'rejected':
			    # 	order.write({'rejected_date':datetime.now()})

			    

			if dispatch_info:
				dispatch_date = datetime.now()
				order.write({'dispatch_status':dispatch_info['dispatch_state']})
				if order.dispatch_status == 'dispatch' and order.dispatch_date == False :
					order.write({'dispatch_date':dispatch_date})
				# else:
				# 	order.write({'dispatch_date':None})


			if rejected_reason:
				order.write({'rejected_reason':rejected_reason['reject_reason']})
		return True



	@http.route(['/submit/'], type='json', auth='public')
	def update_data(self,  advantages=None, **kw):
		# print('$$$$$$$$$$$$$$$$$$$$$$$', self)

		vendor_inputs = self.update_vendor_inputs(advantages, no_write=True, **kw)

		return vendor_inputs


	@http.route(['/my/purchase', '/my/purchase/page/<int:page>'], type='http', auth="user", website=True)
	def portal_my_purchase_orders(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
		values = self._prepare_portal_layout_values()
		partner = request.env.user.partner_id
		PurchaseOrder = request.env['purchase.order']

		domain = []

		archive_groups = self._get_archive_groups('purchase.order', domain)
		if date_begin and date_end:
		    domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

		searchbar_sortings = {
		    'date': {'label': _('Newest'), 'order': 'create_date desc, id desc'},
		    'name': {'label': _('Name'), 'order': 'name asc, id asc'},
		    'amount_total': {'label': _('Total'), 'order': 'amount_total desc, id desc'},
		}
		# default sort by value
		if not sortby:
		    sortby = 'date'
		order = searchbar_sortings[sortby]['order']

		searchbar_filters = {
		    'all': {'label': _('All'), 'domain': [('state', 'in', ['purchase', 'done', 'cancel','closed'])]},
		    'purchase': {'label': _('Purchase Order'), 'domain': [('state', '=', 'purchase')]},
		    'cancel': {'label': _('Cancelled'), 'domain': [('state', '=', 'cancel')]},
		    'done': {'label': _('Locked'), 'domain': [('state', '=', 'done')]},
		    'closed': {'label': _('Closed'), 'domain': [('state', '=', 'closed')]},
		}
		# default filter by value
		if not filterby:
		    filterby = 'all'
		domain += searchbar_filters[filterby]['domain']

		# count for pager
		purchase_count = PurchaseOrder.search_count(domain)
		# make pager
		pager = portal_pager(
		    url="/my/purchase",
		    url_args={'date_begin': date_begin, 'date_end': date_end},
		    total=purchase_count,
		    page=page,
		    step=self._items_per_page
		)
		# search the purchase orders to display, according to the pager data
		orders = PurchaseOrder.search(
		    domain,
		    order=order,
		    limit=self._items_per_page,
		    offset=pager['offset']
		)
		request.session['my_purchases_history'] = orders.ids[:100]

		values.update({
		    'date': date_begin,
		    'orders': orders,
		    'page_name': 'purchase',
		    'pager': pager,
		    'archive_groups': archive_groups,
		    'searchbar_sortings': searchbar_sortings,
		    'sortby': sortby,
		    'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
		    'filterby': filterby,
		    'default_url': '/my/purchase',
		})
		return request.render("purchase.portal_my_purchase_orders", values)
