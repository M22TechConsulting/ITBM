from odoo import api, fields, models

class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    x_product_guarantee_id = fields.Many2one(comodel_name="product.guarantee", string="Garantía")
    x_guarantee_in_picking_id = fields.Many2one(comodel_name="stock.picking", string="Recepción de garantía")
    x_guarantee_denied_id = fields.Many2one(comodel_name="stock.picking", string="Garantía denegada")
    x_guarantee_supplier_id = fields.Many2one(comodel_name="stock.picking", string="Garantía a proveedor")

    @api.onchange("stage_id","x_product_guarantee_id")
    def _onchange_stage_id_guarantee(self):
        for rec in self:
            ticket_id = rec.env["helpdesk.ticket"].sudo().browse(rec.ids)
            if ticket_id and rec.x_product_guarantee_id:
                message = f"""Tu garantía se encuentra en la etapa {rec.stage_id.name}."""
                ticket_id.sudo().message_post(body=message, message_type='comment', subtype_xmlid='mail.mt_comment')

    def denied_guarantee(self):
        for rec in self:
            picking_in = rec.env['stock.picking'].create({
                'partner_id': rec.partner_id.id,
                'picking_type_id': rec.company_id.x_guarantee_picking_type_out_id.id,
                'location_id': rec.company_id.x_guarantee_picking_type_out_id.default_location_src_id.id,
                'location_dest_id': rec.company_id.x_guarantee_picking_type_out_id.default_location_dest_id.id,
            })
            move_line_paw = self.env['stock.move.line'].create({
                'product_id': rec.product_id.id,
                'product_uom_id': rec.product_id.uom_id.id,
                'picking_id': picking_in.id,
                'qty_done': 1,
                'location_id': rec.company_id.x_guarantee_picking_type_out_id.default_location_src_id.id,
                'location_dest_id': rec.company_id.x_guarantee_picking_type_out_id.default_location_dest_id.id,
                'lot_id': rec.lot_id.id
            })

            rec.x_guarantee_denied_id = picking_in.id

    def create_receipts_guarantee(self):
        for rec in self:
            picking_in = rec.env['stock.picking'].create({
                'partner_id': rec.partner_id.id,
                'picking_type_id': rec.company_id.x_guarantee_picking_type_in_id.id,
                'location_id': rec.company_id.x_guarantee_picking_type_in_id.default_location_src_id.id,
                'location_dest_id': rec.company_id.x_guarantee_picking_type_in_id.default_location_dest_id.id,
            })
            move_line_paw = self.env['stock.move.line'].create({
                'product_id': rec.product_id.id,
                'product_uom_id': rec.product_id.uom_id.id,
                'picking_id': picking_in.id,
                'qty_done': 1,
                'location_id': rec.company_id.x_guarantee_picking_type_in_id.default_location_src_id.id,
                'location_dest_id': rec.company_id.x_guarantee_picking_type_in_id.default_location_dest_id.id,
                'lot_id': rec.lot_id.id
            })
            rec.x_guarantee_in_picking_id = picking_in.id


    def open_guarantee_in(self):
        return {
            'name': ('Recepción de garantía'),
            'view_mode': 'form',
            'view_id': self.env.ref('stock.view_picking_form').id,
            'res_model': 'stock.picking',
            'type': 'ir.actions.act_window',
            'res_id': self.x_guarantee_in_picking_id.id
        }

    def open_denied_guarantee(self):
        return {
            'name': ('Garantía denegada'),
            'view_mode': 'form',
            'view_id': self.env.ref('stock.view_picking_form').id,
            'res_model': 'stock.picking',
            'type': 'ir.actions.act_window',
            'res_id': self.x_guarantee_denied_id.id
        }

    def open_supplier_guarantee_picking(self):
        return {
            'name': ('Garantía proveedor'),
            'view_mode': 'form',
            'view_id': self.env.ref('stock.view_picking_form').id,
            'res_model': 'stock.picking',
            'type': 'ir.actions.act_window',
            'res_id': self.x_guarantee_supplier_id.id
        }

    def open_supplier_guarantee(self):
        return {
            'name': ('Garantía proveedor'),
            'view_mode': 'form',
            'view_id': self.env.ref('custom_product_guarantee.product_guarantee_shipping_supplier_view_form').id,
            'res_model': 'product.guarantee.shipping.supplier',
            'type': 'ir.actions.act_window',
            'context': {'default_ticket_id': self.id},
            'target': 'new'
        }

