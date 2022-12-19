# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ProductGuaranteeShippingSupplier(models.TransientModel):
    _name = 'product.guarantee.shipping.supplier'
    _description = 'Envío de garantía a proveedor'

    partner_id = fields.Many2one(comodel_name="res.partner", string="Proveedor")
    ticket_id = fields.Many2one(comodel_name="helpdesk.ticket", string="Ticket")

    def create_supplier_guarantee(self):
        for rec in self:
            picking_out= rec.env['stock.picking'].create({
                'partner_id': rec.partner_id.id,
                'picking_type_id': rec.ticket_id.company_id.x_guarantee_picking_type_out_supplier_id.id,
                'location_id': rec.ticket_id.company_id.x_guarantee_picking_type_out_supplier_id.default_location_src_id.id,
                'location_dest_id': rec.ticket_id.company_id.x_guarantee_picking_type_out_supplier_id.default_location_dest_id.id,
            })
            move_line_paw = self.env['stock.move.line'].create({
                'product_id': rec.ticket_id.product_id.id,
                'product_uom_id': rec.ticket_id.product_id.uom_id.id,
                'picking_id': picking_out.id,
                'qty_done': 1,
                'location_id': rec.ticket_id.company_id.x_guarantee_picking_type_out_supplier_id.default_location_src_id.id,
                'location_dest_id': rec.ticket_id.company_id.x_guarantee_picking_type_out_supplier_id.default_location_dest_id.id,
                'lot_id': rec.ticket_id.lot_id.id
            })
            rec.ticket_id.x_guarantee_supplier_id = picking_out.id



