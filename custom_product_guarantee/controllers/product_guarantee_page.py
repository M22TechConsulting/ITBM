from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError, MissingError, ValidationError

import datetime


class Guarantee(http.Controller):



    @http.route("/guarantee_webform", type="http", auth="user", website=True)
    def guarante_webform(self, **kwargs):

        sale_ids = request.env["sale.order"].sudo().search([("partner_id","=", request.env.user.partner_id.id)])
        lot_ids = sale_ids.order_line.mapped("move_ids").mapped("lot_ids")
        product_ids = lot_ids.mapped("product_id")

        vals = {
            "product_ids": product_ids,
            "accessories": request.env['product.accessories'].sudo().search([]),
            "sale_ids": sale_ids,
            "lot_ids": lot_ids
        }
        return request.render("custom_product_guarantee.create_guarantee", vals)

    @http.route("/create/webguarantee", type="http", auth="user", website=True)
    def create_guarantee(self, **kwargs):
        partner_id = request.env.user.partner_id

        keys = kwargs.keys()

        accessory_ids = []
        for key in keys:
            if "accessory" in key:
                accessory_ids.append(int(kwargs[key]))

        values_guarantee = {
            "user_id": request.env.user.id,
            "lot_id": int(kwargs["lot_id"]),
            "accessory_ids": accessory_ids,
            "date": datetime.datetime.now(),
            "sale_id": int(kwargs["sale_id"]),
            "product_id": int(kwargs["product_id"]),
            "description": kwargs["description"]
        }

        guarantee_id = request.env["product.guarantee"].sudo().create(values_guarantee)
        team_id = request.env.ref("custom_product_guarantee.product_guarantee_helpdesk_team")
        ticket_type_id = request.env.ref("custom_product_guarantee.product_guarantee_helpdesk_ticket_type")


        values_ticket = {
            "partner_id": request.env.user.partner_id.id,
            "partner_email": partner_id.email,
            "x_product_guarantee_id": guarantee_id.id,
            "name": f"Garantía {guarantee_id.name}",
            "product_id": int(kwargs["product_id"]),
            "sale_order_id": int(kwargs["sale_id"]),
            "team_id": team_id.id,
            "description": kwargs["description"],
            "ticket_type_id": ticket_type_id.id,
            "lot_id": int(kwargs["lot_id"]),
        }
        ticket_id = request.env["helpdesk.ticket"].sudo().create(values_ticket)
        guarantee_id.ticket_id = ticket_id.id
        ticket_id.sudo().create_receipts_guarantee()

        return request.render("custom_product_guarantee.product_guarantee_thanks", {})
