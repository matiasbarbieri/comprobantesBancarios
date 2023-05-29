import pytesseract
import re
import os
from pdf2image import convert_from_path
from PIL import Image

def get_text_from_pdf(bcosantander):
    if bcosantander.endswith('.pdf'):
        pages = convert_from_path(bcosantander, 200)
        image = pages[0]
    elif os.path.isfile(bcosantander):
        image = Image.open(bcosantander)
    else:
        print(f"Error: {bcosantander} is not a valid PDF or image file.")
        return None

    gray_image = image.convert('L')
    text = pytesseract.image_to_string(gray_image, lang='spa')
    # print (text)
    return text

def get_titular_from_text(text):
    pattern = r"Titular cuenta destino\s+(\S+.*)(?=\n)"
    match = re.search(pattern, text)
    if match:
        beneficiario = match.group(1)
        return beneficiario

def get_banco_from_text(text):
    pattern = r"Santander"
    match = re.search(pattern, text)
    if match:
        titular = match.group()
        return titular

def get_cuit_remitente_from_text(text):
    pattern = r"\n([0-9]{2}-[0-9]{8}-[0-9]{1})\n\n"
    match = re.search(pattern, text)
    if match:
        cuit_remitente = match.group(1)
        return cuit_remitente
    else:
        return "Este comprobante no tiene cuit remitente."

def get_fecha_from_text(text):
    pattern = r"Fecha de ejecución\s+(\S+.*)(?=\n)"
    match = re.search(pattern, text)
    if match:
        fecha = match.group(1)
        return fecha

def get_importe_from_text(text):
    pattern = r"Importe debitado\s+(\S+.*)(?=\n)"
    match = re.search(pattern, text)
    if match:
        importe = match.group().strip().replace("Importe debitado $", "")
        return importe

