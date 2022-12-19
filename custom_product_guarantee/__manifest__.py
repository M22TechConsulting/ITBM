# -*- coding: utf-8 -*-
{
    'name': "Garantías de productos",
    'summary': """
        Manejo de garantias de productos.
    """,
    'description': """
        Portal de cliente para el manejo de garantias de productos.
    """,
    'author': "M22",
    'website': "https://www.m22.mx",
    'category': 'Inventory/Inventory',
    'version': '16.0.1',
    'depends': ['base','helpdesk','product','portal','stock','sale','website','helpdesk_stock'],
    'data': [
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        'data/ir_sequence.xml',
        'data/helpdesk_team.xml',
        'data/helpdesk_stage.xml',
        'data/helpdesk_ticket_type.xml',
        'views/res_config_settings.xml',
        'views/product_accessories.xml',
        'views/product_guarantee.xml',
        'views/product_guarentee_portal.xml',
        'views/product_guarantee_page.xml',
        'wizards/product_guarantee_shipping_supplier.xml',
        'views/helpdesk_ticket.xml',
    ],
    'license': 'AGPL-3'
}
