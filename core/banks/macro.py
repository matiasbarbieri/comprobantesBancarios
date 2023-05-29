import pytesseract
import re
import os
from pdf2image import convert_from_path
from PIL import Image

def get_text_from_pdf(bcomacro):
    if bcomacro.endswith('.pdf'):
        pages = convert_from_path(bcomacro, 200)
        image = pages[0]
    elif os.path.isfile(bcomacro):
        image = Image.open(bcomacro)
    else:
        print(f"Error: {bcomacro} is not a valid PDF or image file.")
        return None

    gray_image = image.convert('L')
    text = pytesseract.image_to_string(gray_image, lang='spa')
    # print (text)
    return text

def get_titular_from_text(text):
    pattern = r"\n([A-Z\s\.]+)\n"
    match = re.search(pattern, text)
    if match:
        beneficiario = match.group(1)
        return beneficiario

def get_banco_from_text(text):
    pattern = r"fin\s+(\S+.*)(?=\n)"
    match = re.search(pattern, text)
    if match:
        titular = match.group().strip().replace("fin ", "")
        return titular

def get_cuit_remitente_from_text(text):
    pattern = r"\n([0-9]{2}-[0-9]{8}-[0-9]{1})\n\n"
    match = re.search(pattern, text)
    if match:
        cuit_remitente = match.group(1)
        return cuit_remitente

def get_fecha_from_text(text):
    pattern = r"(\d{2}/\d{2}/\d{4})\s\d{2}:\d{2}\s\d+\n"
    match = re.search(pattern, text)
    if match:
        fecha = match.group(1)
        return fecha

def get_importe_from_text(text):
    pattern = r"([0-9]+\.[0-9]{2})"
    match = re.search(pattern, text)
    if match:
        importe = match.group(1)
        return importe

