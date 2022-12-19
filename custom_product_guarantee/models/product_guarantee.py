# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductGuarantee(models.Model):
    _name = "product.guarantee"
    _description = "Garantía del producto"

    name = fields.Char(string="Referencia")
    user_id = fields.Many2one(comodel_name="res.users",string="Usuario", default=lambda self: self.env.user)
    date = fields.Datetime(string="Fecha")
    product_id = fields.Many2one(comodel_name="product.product")
    lot_id = fields.Many2one(comodel_name="stock.lot", string="IMEI")
    company_id = fields.Many2one(comodel_name="res.company", string="Compañía", default=lambda self: self.env.company)
    accessory_ids = fields.Many2many(comodel_name="product.accessories", string="Accesorios")
    sale_id = fields.Many2one(comodel_name="sale.order", string="#Venta")
    description = fields.Text(string="Descripción")
    ticket_id = fields.Many2one(comodel_name="helpdesk.ticket", string="Ticket")
    stage_id = fields.Many2one(comodel_name="helpdesk.stage", string="Etapa", related="ticket_id.stage_id")

    @api.model
    def create(self, vals_list):
        res = super(ProductGuarantee, self).create(vals_list)
        name = self.env['ir.sequence'].next_by_code('product.guarantee')
        res["name"] = name
        return res

