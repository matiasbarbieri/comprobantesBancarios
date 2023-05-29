import pytesseract
import re
import os
from pdf2image import convert_from_path
from PIL import Image

def get_text_from_pdf(mp):
    if mp.endswith('.pdf'):
        pages = convert_from_path(mp, 200)
        image = pages[0]
        # image.save('image.png', 'PNG') para test
    elif os.path.isfile(mp):
        image = Image.open(mp)
    else:
        print(f"Error: {mp} is not a valid PDF or image file.")
        return None
        
    gray_image = image.convert('L')
    # gray_image.save('gray_image.png', 'PNG') para test
    text = pytesseract.image_to_string(gray_image, lang='spa')
    # print (text)

    return text

def get_titular_from_text(text):
    pattern = r"(.*\n){1}(.*)(\n.*)Cuenta Mercado Pago"
    match = re.search(pattern, text)
    if match:
        titular = match.group(1).rstrip()
        return titular

def get_banco_from_text(text):
    pattern = r"Mercado Pago"
    match = re.search(pattern, text)
    if match:
        banco = match.group()
        return banco

def get_cuit_remitente_from_text(text):
    pattern = r"(\d{2}-\d{8}-\d{1})"
    match = re.search(pattern, text)
    if match:
        cuit_remitente = match.group(1)
        return cuit_remitente

def get_fecha_from_text(text):
    pattern = r"\d{1,2}\s+(?:de\s+)?\w+\s+\d{4}"
    match = re.search(pattern, text)
    if match:
        fecha = match.group()
        return fecha

def get_importe_from_text(text):
    pattern = r"\$\s+(\S+.*)(?=\n)"
    match = re.search(pattern, text)
    if match:
        importe = match.group().strip().replace("$ ", "")
        return importe

def get_coelsa_from_text(text):
    pattern = r"(Caja de ahorro)\n\n(([a-zA-Z0-9]))(\S+.*)(?=\n)"
    match = re.search(pattern, text)
    if match:
        coelsa = match.group(4).strip()
        return coelsa
