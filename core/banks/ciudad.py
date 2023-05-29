import pytesseract
import re
import os
from pdf2image import convert_from_path
from PIL import Image

def get_text_from_pdf(bcociudad):
    if bcociudad.endswith('.pdf'):
        pages = convert_from_path(bcociudad, 200)
        image = pages[0]
    elif os.path.isfile(bcociudad):
        image = Image.open(bcociudad)
    else:
        print(f"Error: {bcociudad} is not a valid PDF or image file.")
        return None

    gray_image = image.convert('L')
    text = pytesseract.image_to_string(gray_image, lang='spa')
    # print (text)
    return text

def get_titular_from_text(text):
    pattern = r"(\S.*)(\d{2}-\d{8}-\d{1})"
    match = re.search(pattern, text)
    if match:
        beneficiario = match.group(1)
        return beneficiario

def get_banco_from_text(text):
    pattern = r"BancoCiudad"
    match = re.search(pattern, text)
    if match:
        titular = match.group()
        return titular

def get_cuit_remitente_from_text(text):
    pattern = r"(\S.*)(\d{2}-\d{8}-\d{1})"
    match = re.search(pattern, text)
    if match:
        cuit_remitente = match.group(2)
        return cuit_remitente
    else:
        return "Este comprobante no tiene cuit remitente."

def get_fecha_from_text(text):
    pattern = r"(\d{1,2}/\d{1,2}/\d{4})"
    match = re.search(pattern, text)
    if match:
        fecha = match.group()
        return fecha

def get_importe_from_text(text):
    pattern = r"\$\s?(\d{1,3}(?:\.\d{3})*,\d{2})"
    match = re.search(pattern, text)
    if match:
        importe = match.group().strip().replace("Importe debitado $", "")
        return importe

