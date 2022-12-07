# -*- coding: utf-8 -*-
{
    'name': "Reporte de lista de precios por producto",
    'summary': """
        Reporte de lista de precios por producto en detalle.        
    """,
    'description': """
        Reporte de lista de precios por producto en detalle por sus atributos y sus precios
        en una sola celda y su impresión en excel.
    """,
    'author': "M22",
    'website': "https://m22.mx",
    'category': 'Sales',
    'version': '16.0.1',
    'depends': ['base','product','stock','report_xlsx'],
    'data': [
        'reports/product_pricelist_report_xlsx.xml'
    ],
    'license': 'AGPL-3'
}
