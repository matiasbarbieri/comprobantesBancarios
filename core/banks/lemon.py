import pytesseract
import re
import os
from pdf2image import convert_from_path
from PIL import Image

def get_text_from_pdf(bcolemon):
    if bcolemon.endswith('.pdf'):
        pages = convert_from_path(bcolemon, 200)
        image = pages[0]
    elif os.path.isfile(bcolemon):
        image = Image.open(bcolemon)
    else:
        print(f"Error: {bcolemon} is not a valid PDF or image file.")
        return None

    gray_image = image.convert('L')
    text = pytesseract.image_to_string(gray_image, lang='spa')
    # print (text)
    return text

def get_titular_from_text(text):
    pattern = r"(Enviado por\s)(\S+.*)(?=\n)"
    match = re.search(pattern, text)
    if match:
        beneficiario = match.group(2)
        return beneficiario

def get_banco_from_text(text):
    pattern = r"LEMON"
    match = re.search(pattern, text)
    if match:
        banco = "Lemon"
        return banco

def get_cuit_remitente_from_text(text):
    pattern = r"(CUIT\s)(\S+.*)(?=\n)"
    match = re.search(pattern, text)
    if match:
        cuit_remitente = match.group(2)
        return cuit_remitente

def get_fecha_from_text(text):
    pattern = r"\d{1,2}\s+\w{3,}"
    match = re.search(pattern, text)
    if match:
        fecha = match.group()
        return fecha

def get_importe_from_text(text):
    pattern = r"(ARS\s)(\S.+)"
    match = re.search(pattern, text)
    if match:
        importe = match.group(2)
        return importe

