# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResCompany(models.Model):
    _inherit = "res.company"

    x_guarantee_picking_type_in_id = fields.Many2one(comodel_name="stock.picking.type", string="Operación de recepción")
    x_guarantee_picking_type_out_id = fields.Many2one(comodel_name="stock.picking.type", string="Operación de entrega")
    x_guarantee_picking_type_out_supplier_id = fields.Many2one(comodel_name="stock.picking.type", string="Operación de entrega a proveedor")