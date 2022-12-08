# -*- coding: utf-8 -*-

from odoo import api, fields, models
import base64
import io


class ProductPricelistReportXLSX(models.AbstractModel):
    _name = 'report.product_pricelist_report.product_pricelist_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Listas de precios por producto'

    def generate_xlsx_report(self, workbook, data, lines):
        """Generar el informe de lista de precios en formato xlsx de excel.
        :param workbook: Area de trabajo del informe xlsx.
        :param data:
        :param lines: Registros de donde proviene la información.
        :return:
        """
        # Creación de nuestra hoja de excel
        sheet = workbook.add_worksheet('Reporte')
        header_columns_format = workbook.add_format({'font_size': 11, 'align': 'left', 'bg_color': '#213E8B', 'font_color': 'white', 'border': 1})
        header_columns_format.set_align("vcenter")

        # Anchura de columnas
        sheet.set_column(0, 0, 17)
        sheet.set_column(1, 1, 50)
        sheet.set_column(2, 50, 25)
        # Altura de la celda
        sheet.set_row(3, 30)

        # Letras de las celdas
        alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)]

        # Se obtienen las reglas de lista de precios de los productos
        if data.get("context").get("pricelist"):
            pricelist_ids = data.get("context").get("pricelist")
            pricelist_ids = self.env["product.pricelist"].sudo().browse(pricelist_ids)
            pricelist_ids = pricelist_ids.mapped("item_ids")
        else:
            pricelist_ids = self._get_product_pricelist_records(lines)

        # Se obtienen los atributos
        if data.get("context").get("attributes"):
            attribute_ids = data.get("context").get("attributes")
            attribute_ids = self.env["product.attribute"].sudo().browse(attribute_ids)
        else:
            attribute_ids = lines.mapped("attribute_line_ids").mapped("attribute_id")

        # Se obtiene el nombre de las listas de precios
        pricelist_columns = pricelist_ids.mapped("pricelist_id").mapped("name")
        attribute_columns = attribute_ids.mapped("name")
        columns = ["Descripción", "Nombre"] + pricelist_columns + ["Colores Disp. Variantes"] + attribute_columns
        # Se obtiene el logo de la empresa para colocarlo en el excel
        if self.env.company.logo:
            image_width = 140.0
            image_height = 182.0
            cell_width = 100
            cell_height = 150
            x_scale = cell_width / image_width
            y_scale = cell_height / image_height
            company_image = io.BytesIO(base64.b64decode(self.env.company.logo))
            sheet.insert_image(0, 0, "image.png", {'image_data': company_image, 'object_position': 2, 'x_scale': x_scale, 'y_scale': y_scale})
        # Se colocan dinamicamente las listas
        for column in range(len(columns)):
            sheet.write(f'{alphabet[column].upper()}4', ''.join([i for i in columns[column] if not i.isdigit()]), header_columns_format)
        # Se comienza en el la celda despues de las columnas
        row = 5
        index = 0
        # Se escribe en las celdas los valores
        for line in lines:
            sheet.write(f'{alphabet[index].upper()}{row}', line.display_name)
            sheet.write(f'{alphabet[index + 1].upper()}{row}', line.name)
            columns_count = 2
            for pricelist in pricelist_ids.mapped("pricelist_id"):
                price_ids = pricelist.item_ids.filtered(lambda price: price.product_tmpl_id.id == line.id and price.fixed_price > 0)
                product_price = price_ids[0].fixed_price if price_ids else 0
                sheet.write(f'{alphabet[index + columns_count].upper()}{row}', product_price)
                columns_count += 1

            #Agregamos las variantes y sus atributos de colores
            if len(line.product_variant_ids) > 1:
                variant_values = line.product_variant_ids.mapped("product_template_variant_value_ids").filtered(lambda attr: "Color" in attr.display_name).mapped("name")
            elif len(line.product_variant_ids) == 1:
                variant_values = line.product_variant_ids.mapped("product_template_attribute_value_ids").filtered(lambda attr: "Color" in attr.display_name).mapped("name")
            else:
                variant_values = []

            sheet.write(f'{alphabet[index + columns_count].upper()}{row}', ",".join(variant_values))
            columns_count += 1
            for attribute_id in attribute_ids:
                attribute = line.attribute_line_ids.filtered(lambda attribute: attribute.attribute_id.id == attribute_id.id)
                sheet.write(f'{alphabet[index + columns_count].upper()}{row}', ",".join(attribute.value_ids.mapped("name")))
                columns_count += 1
            row += 1

    def _get_product_pricelist_records(self, lines):
        return self.env["product.pricelist.item"].sudo().search([("product_tmpl_id.id", "in", lines.ids), ("pricelist_id.active", "=", True)])
