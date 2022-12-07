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
        header_columns_format = workbook.add_format({'font_size': 11, 'align': 'left','bg_color': '#213E8B', 'font_color': 'white', 'border': 1})
        header_columns_format.set_align("vcenter")

        # Anchura de columnas
        sheet.set_column(0, 0, 17)
        sheet.set_column(1, 1, 50)
        sheet.set_column(2, 50, 25)
        # Altura de la celda
        sheet.set_row(3, 30)

        #Letras de las celdas
        alphabet = [chr(i) for i in range(ord('a'), ord('z') + 1)]

        #Se obtienen las reglas de lista de precios de los productos
        pricelist_ids = self._get_product_pricelist_records(lines)
        #Se obtiene el nombre de las listas de precios
        pricelist_columns = pricelist_ids.mapped("pricelist_id").mapped("name")
        columns = ["Descripción","Nombre"] + pricelist_columns + ["Colores Disp. Variantes"]
        #Se obtiene el logo de la empresa para colocarlo en el excel
        if self.env.company.logo:
            company_image = io.BytesIO(base64.b64decode(self.env.company.logo))
            sheet.insert_image(0,0,"image.png",{'image_data': company_image, 'x_scale': 0.8, 'y_scale': 0.8})
        #Se colocan dinamicamente las listas
        for column in range(len(columns)):
            sheet.write(f'{alphabet[column].upper()}4', ''.join([i for i in columns[column] if not i.isdigit()]), header_columns_format)
        #Se comienza en el la celda despues de las columnas
        row = 5
        index = 0
        #Se escribe en las celdas los valores
        for line in lines:
            sheet.write(f'{alphabet[index].upper()}{row}', line.display_name)
            sheet.write(f'{alphabet[index + 1].upper()}{row}', line.name)
            columns_count = 2
            for pricelist in pricelist_ids.mapped("pricelist_id"):
                price_ids = pricelist.item_ids.filtered(lambda price: price.product_tmpl_id.id == line.id and price.fixed_price > 0)
                product_price = price_ids[0].fixed_price if price_ids else 0
                sheet.write(f'{alphabet[index + columns_count].upper()}{row}', product_price)
                columns_count += 1
            sheet.write(f'{alphabet[index + columns_count].upper()}{row}', ",".join(line.attribute_line_ids.filtered(lambda attr: attr.attribute_id.name == 'Color').mapped("value_ids").mapped('name')))
            row += 1

    def _get_product_pricelist_records(self, lines):
        return self.env["product.pricelist.item"].sudo().search([("product_tmpl_id.id","in",lines.ids),("pricelist_id.active","=",True)])


