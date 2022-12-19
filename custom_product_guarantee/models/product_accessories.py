from odoo import api, fields, models

class ProductAccessories(models.Model):
    _name = 'product.accessories'
    _description = 'Accesorio del producto'

    name = fields.Char(string="Nombre")

