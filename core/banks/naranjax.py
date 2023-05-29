import pytesseract
import re
import os
from pdf2image import convert_from_path
from PIL import Image

def get_text_from_pdf(naranja):
    if naranja.endswith('.pdf'):
        pages = convert_from_path(naranja, 200)
        image = pages[0]
    elif os.path.isfile(naranja):
        image = Image.open(naranja)
    else:
        print(f"Error: {naranja} is not a valid PDF or image file.")
        return None

    gray_image = image.convert('L')
    text = pytesseract.image_to_string(gray_image, lang='spa')
    # print (text)
    return text

def get_titular_from_text(text):
    pattern = r"Desde\n(.+)"
    match = re.search(pattern, text)
    if match:
        beneficiario = match.group(1)
        return beneficiario

def get_banco_from_text(text):
    pattern = r"Naranja X"
    match = re.search(pattern, text)
    if match:
        banco = "Naranja X"
        return banco

def get_cuit_remitente_from_text(text):
    pattern = r"CUIT de origen\n(.*)"
    match = re.search(pattern, text)
    if match:
        cuit_remitente = match.group(1)
        return cuit_remitente

def get_fecha_from_text(text):
    pattern = r"(\d{1,2}/\w{3}/\d{4})"
    match = re.search(pattern, text)
    if match:
        fecha = match.group()
        return fecha

def get_importe_from_text(text):
    pattern = r"\$\s?(\d{1,3}(?:\.\d{3})*,\d{2})"
    match = re.search(pattern, text)
    if match:
        importe = match.group(1)
        return importe

