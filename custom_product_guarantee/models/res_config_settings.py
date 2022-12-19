from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    x_guarantee_picking_type_in_id = fields.Many2one(comodel_name="stock.picking.type", related="company_id.x_guarantee_picking_type_in_id", string="Operación de recepción", readonly=False)
    x_guarantee_picking_type_out_id = fields.Many2one(comodel_name="stock.picking.type", related="company_id.x_guarantee_picking_type_out_id", string="Operación de entrega", readonly=False)
    x_guarantee_picking_type_out_supplier_id = fields.Many2one(comodel_name="stock.picking.type", related="company_id.x_guarantee_picking_type_out_supplier_id", string="Operación de entrega a proveedor", readonly=False)
