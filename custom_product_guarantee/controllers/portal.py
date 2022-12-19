from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.portal.controllers import portal
from odoo.tools import groupby as groupbyelem
from odoo.osv.expression import AND, OR
from operator import itemgetter
from datetime import datetime
from odoo import http, _
from odoo.http import request


class CustomerPortal(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        """Se preparan los valores del portal al que tendra acceso el usuario al iniciar sesión
        :param counters:
        :return:
        """
        values = super()._prepare_home_portal_values(counters)
        if 'guarantee_count' in counters:
            domain = self._get_portal_default_domain()
            product_guarantee = request.env['product.guarantee']
            count = product_guarantee.search_count(domain) if product_guarantee.check_access_rights('read', raise_exception=False) else 0
            values['guarantee_count'] = count
        return values

    def _get_portal_default_domain(self):
        my_user = request.env.user
        return [
            ('user_id', '=', my_user.id),
        ]

    def _get_guarantee_search_domain(self, search_in, search):
        search_domain = []
        if search_in in ('all', 'name'):
            search_domain = OR([search_domain, [('name', 'ilike', search)]])
        if search_in in ('all', 'product_id'):
            search_domain = OR([search_domain, [('product_id', 'ilike', search)]])
        if search_in in ('all', 'lot_id'):
            search_domain = OR([search_domain, [('lot_id', 'ilike', search)]])
        return search_domain

    def _guarantee_get_groupby_mapping(self):
        return {
            'user_id': 'user_id',
        }

    @http.route(['/my/guarantee',
                 '/my/guarantee/page/<int:page>',
                 ], type='http', auth='user', website=True)
    def portal_my_guarantee(self, page=1, sortby=None, filterby=None, search=None, search_in='all', groupby='none', **kwargs):
        values = self._prepare_portal_layout_values()
        # Sudo para acceder al nombre, producto y imei de la para la agrupación garantia
        guarantee = request.env['product.guarantee'].sudo()
        domain = self._get_portal_default_domain()

        searchbar_sortings = {
            'date': {'label': _('Date'), 'order': 'date'},
            'name': {'label': _('Name'), 'order': 'name'},
        }

        searchbar_inputs = {
            'all': {'label': _('Buscar todo'), 'input': 'all'},
            'name': {'label': _('Buscar por nombre'), 'input': 'name'},
            'product_id': {'label': _('Buscar por producto'), 'input': 'product_id'},
            'lot_id': {'label': _('Buscar por IMEI'), 'input': 'lot_id'}
        }

        searchbar_groupby = {
            'none': {'label': _('None'), 'input': 'none'},
            'product_id': {'label': _('Producto'), 'input': 'product_id'},
            'stage': {'label': _('Etapa'), 'input': 'stage_id'}
        }

        searchbar_filters = {
            'all': {'label': _("All"), 'domain': []},
            'upcoming': {'label': _("Upcoming"), 'domain': [('date', '>=', datetime.today())]},
            'past': {'label': _("Past"), 'domain': [('date', '<', datetime.today())]},
        }

        if not sortby:
            sortby = 'date'

        sort_order = searchbar_sortings[sortby]['order']
        groupby_mapping = self._guarantee_get_groupby_mapping()
        groupby_field = groupby_mapping.get(groupby, None)

        if groupby_field is not None and groupby_field not in guarantee._fields:
            raise ValueError(_("The field '%s' does not exist in the targeted model", groupby_field))
        order = '%s, %s' % (groupby_field, sort_order) if groupby_field else sort_order
        if not filterby:
            filterby = 'all'
        domain = AND([domain, searchbar_filters[filterby]['domain']])

        if search and search_in:
            domain = AND([domain, self._get_guarantee_search_domain(search_in, search)])

        guarantee_count = guarantee.search_count(domain)

        pager = portal_pager(
            url="/my/guarantee",
            url_args={'sortby': sortby, 'search_in': search_in, 'search': search, 'groupby': groupby},
            total=guarantee_count,
            page=page,
            step=self._items_per_page
        )

        guarantee_ids = guarantee.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])

        grouped_guarantee = False

        # If not False, this will contain a list of tuples (record of groupby, recordset of events):
        # [(res.users(2), calendar.event(1, 2)), (...), ...]
        if groupby_field:
            grouped_appointments = [(g, guarantee.concat(*events)) for g, events in groupbyelem(guarantee_ids, itemgetter(groupby_field))]

        values.update({
            'guarantee_ids': guarantee_ids,
            'grouped_guarantee': grouped_guarantee,
            'page_name': 'guarantee',
            'pager': pager,
            'default_url': '/my/guarantee',
            'searchbar_sortings': searchbar_sortings,
            'search_in': search_in,
            'search': search,
            'sortby': sortby,
            'groupby': groupby,
            'filterby': filterby,
            'searchbar_inputs': searchbar_inputs,
            'searchbar_groupby': searchbar_groupby,
            'searchbar_filters': searchbar_filters,
        })
        return request.render("custom_product_guarantee.portal_my_guarantee", values)















    #
    #
    # def _prepare_my_guarantee_values(self, template, page, sortby, url, history, page_name, key):
    #     values = self._prepare_portal_layout_values()
    #     guarantee_id = request.env['product.guarantee'].sudo()
    #
    #     domain = self._get_portal_default_domain()
    #
    #     searchbar_sortings = {
    #         'date': {'label': 'Más reciente', 'order': 'date desc, id desc'},
    #         'name': {'label': 'IMEI', 'order': 'name asc, id asc'},
    #     }
    #
    #     searchbar_inputs = {
    #         'all': {'label': _('Search in All'), 'input': 'all'},
    #         'name': {'label': _('Search in Name'), 'input': 'name'},
    #         'responsible': {'label': _('Search in Responsible'), 'input': 'responsible'},
    #         'description': {'label': _('Search in Description'), 'input': 'description'}
    #     }
    #
    #     searchbar_groupby = {
    #         'none': {'label': _('None'), 'input': 'none'},
    #         'responsible': {'label': _('Responsible'), 'input': 'responsible'},
    #     }
    #
    #     searchbar_filters = {
    #         'upcoming': {'label': _("Upcoming"), 'domain': [('start', '>=', datetime.today())]},
    #         'past': {'label': _("Past"), 'domain': [('start', '<', datetime.today())]},
    #         'all': {'label': _("All"), 'domain': []},
    #     }
    #
    #     if not sortby:
    #         sortby = 'date'
    #     sort_order = searchbar_sortings[sortby]['order']
    #
    #     order = searchbar_sortings[sortby]['order']
    #
    #     count = guarantee_id.search_count([
    #         ('user_id', '=', request.env.user.id),
    #     ])
    #
    #     pager = portal_pager(
    #         url=url,
    #         url_args={'sortby': sortby},
    #         total=count,
    #         page=page,
    #         step=self._items_per_page
    #     )
    #
    #     product_guarantee_ids = guarantee_id.search(
    #         [('user_id', '=', request.env.user.id)],
    #         order=order,
    #         limit=self._items_per_page,
    #         offset=pager['offset']
    #     )
    #
    #     request.session[history] = product_guarantee_ids.ids[:100]
    #
    #     values.update({
    #         key: product_guarantee_ids,
    #         'page_name': page_name,
    #         'pager': pager,
    #         'searchbar_sortings': searchbar_sortings,
    #         'sortby': sortby,
    #         'default_url': url,
    #     })
    #
    #     return request.render(template, values)
    #
    # @http.route(['/my/product_guarantee_portal', '/my/product_guarantee_portal/page/<int:page>'], type='http', auth="user", website=True)
    # def portal_my_guarantee(self, page=1, sortby=None, **kw):
    #     return self._prepare_my_guarantee_values(
    #         "custom_product_guarantee.portal_my_guarantee",
    #         page,
    #         sortby,
    #         "/my/product_guarantee_portal",
    #         'my_product_guarantee_portal_history',
    #         'product_guarantee',
    #         'product_guarantee_ids'
    #     )
    #
    #
    #
