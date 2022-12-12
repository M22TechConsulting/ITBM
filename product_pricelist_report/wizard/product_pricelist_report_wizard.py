# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ProductPricelistReportWizard(models.TransientModel):
    _name = 'product.pricelist.report.wizard'
    _description = 'Generador de reporte de lista de precios'

    name = fields.Char(string="Nombre", default="Reporte de lista de precios")
    product_ids = fields.Many2many(comodel_name="product.template", string="Productos")
    pricelist_ids = fields.Many2many(comodel_name="product.pricelist", string="Lista de precios")
    company_id = fields.Many2one(comodel_name="res.company", string="Compañía", default=lambda self: self.env.company)
    attribute_ids = fields.Many2many(comodel_name="product.attribute", string="Atributos")

    def generate_report_xlsx(self):
        self = self.with_context(pricelist=self.pricelist_ids.ids, attributes=self.attribute_ids.ids)
        return self.env.ref("product_pricelist_report.product_pricelist_report_xlsx").report_action(self.product_ids, data=self.env.context)

    # @api.onchange('product_ids')
    # def _domain_product_pricelist_onchange(self):
    #     if self.product_ids:
    #         pricelist_ids = self.env["product.pricelist.item"].sudo().search([("product_tmpl_id.id", "in", self.product_ids.ids), ("pricelist_id.active", "=", True)]).mapped("pricelist_id")
    #     else:
    #         pricelist_ids = self.env["product.pricelist.item"].sudo().search([("pricelist_id.active", "=", True)]).mapped("pricelist_id")
    #     attribute_ids = self.env["product.attribute"].sudo().search([("id","in",self.product_ids.mapped("attribute_line_ids").mapped("attribute_id").ids)])
    #
    #     return {'domain': {'pricelist_ids': [('id', 'in', pricelist_ids.ids)], 'attribute_ids': [("id","in",attribute_ids.ids)]}}

    @api.onchange('pricelist_ids')
    def _onchancge_pricelist_ids(self):
        self.product_ids = self.pricelist_ids.mapped("item_ids").mapped("product_tmpl_id").mapped("id")

