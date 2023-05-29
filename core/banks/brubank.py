import pytesseract
import re
import os
from pdf2image import convert_from_path
from PIL import Image

def get_text_from_pdf(bcobrubank):
    if bcobrubank.endswith('.pdf'):
        pages = convert_from_path(bcobrubank, 200)
        image = pages[0]
    elif os.path.isfile(bcobrubank):
        image = Image.open(bcobrubank)
    else:
        print(f"Error: {bcobrubank} is not a valid PDF or image file.")
        return None

    gray_image = image.convert('L')
    gray_image.save('gray_image.png', 'PNG') 
    text = pytesseract.image_to_string(gray_image, lang='spa')
    # print (text)
    return text

def get_titular_from_text(text):
    pattern = r"(Envío de dinero a)\n\n(.+)"
    match = re.search(pattern, text)
    if match:
        beneficiario = match.group(2)
        return beneficiario

def get_banco_from_text(text):
    pattern = r"brubank"
    match = re.search(pattern, text)
    if match:
        banco = "brubank"
        return banco

def get_cuit_remitente_from_text(text):
    pattern = r"(CUIT\s)+(\S+.*)(?=\n)"
    match = re.search(pattern, text)
    if match:
        cuit_remitente = match.group(2)
        return cuit_remitente

def get_fecha_from_text(text):
    pattern = r"(\d{1,2}\s+(de\s)?\w+)"
    match = re.search(pattern, text)
    if match:
        fecha = match.group(1)
        return fecha

def get_importe_from_text(text):
    pattern = r"\$\s?(\d{1,3}(?:\.\d{3})*,\d{2})"
    match = re.search(pattern, text)
    if match:
        importe = match.group(1)
        return importe

