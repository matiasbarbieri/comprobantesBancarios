import pytesseract
import re
import os
from pdf2image import convert_from_path
from PIL import Image
from . import bbva, macro, nacion, santander, santander2, mercadopago, naranjax, brubank, lemon, icbc, galicia, ciudad


def get_banco_del_comprobante(pdf_path):
    bancosTotales = [bbva, macro, nacion, santander, santander2, mercadopago, naranjax, brubank, lemon, icbc, galicia, ciudad]

    for bancoIndividual in bancosTotales:
        lectura = bancoIndividual.get_text_from_pdf(pdf_path)
        obtener_banco = bancoIndividual.get_banco_from_text(lectura)

        if obtener_banco:
            print(f"Se encontró un banco válido: {obtener_banco}")
            # Se encontró un banco válido, ejecutar las funciones restantes del archivo
            titular = bancoIndividual.get_titular_from_text(lectura)
            print(f"Titular: {titular}")
            cuit_remitente = bancoIndividual.get_cuit_remitente_from_text(lectura)
            print(f"CUIT: {cuit_remitente}")
            banco_obtenido = bancoIndividual.get_banco_from_text(lectura)
            print(f"Banco: {banco_obtenido}")
            fecha = bancoIndividual.get_fecha_from_text(lectura)
            print(f"Fecha: {fecha}")
            importe = bancoIndividual.get_importe_from_text(lectura)
            print(f"Importe: {importe}")

            # print(f"Titular: {titular}, Banco: {obtener_banco}, CUIT: {cuit_remitente}, Fecha: {fecha}, Importe: {importe}")
            
            # Construir el diccionario de contexto con los datos obtenidos
            context = {
                'titular': titular,
                'banco': banco_obtenido,
                'cuit_remitente': cuit_remitente,
                'fecha': fecha,
                'importe': importe
            }
            
            return context

    return None
