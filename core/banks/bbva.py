import pytesseract
import re
import os
from pdf2image import convert_from_path
from PIL import Image

def get_text_from_pdf(pdf_path):
    if pdf_path.endswith('.pdf'):
        pages = convert_from_path(pdf_path, 200)
        image = pages[0]
        # image.save('image.png', 'PNG') para test
    elif os.path.isfile(pdf_path):
        image = Image.open(pdf_path)
    else:
        print(f"Error: {pdf_path} is not a valid PDF or image file.")
        return None
        
    gray_image = image.convert('L')
    # gray_image.save('gray_image.png', 'PNG') para test
    text = pytesseract.image_to_string(gray_image, lang='spa')
    print (text)

    return text

def get_titular_from_text(text):
    pattern = r"Ordenante\s+(\S+.*)(?=\n)" #transferencia
    match = re.search(pattern, text)
    if match:
        titular = match.group().strip().replace("Ordenante ", "").replace(" Fecha", "")
        return titular
    else:
        pattern = r"(Titular Cta\. Débito:)\s+(\S+\s+\S+\s*\S*)\s+\d+" #debito
        match = re.search(pattern, text)
        if match:
            titular = match.group(2)
            return titular


def get_banco_from_text(text):
    pattern = r"BBVA"
    match = re.search(pattern, text)
    if match:
        banco = match.group()
        return banco

def get_cuit_remitente_from_text(text):
    pattern = r"CUIT\s+(\S+.*)(?=\n)"
    match = re.search(pattern, text)
    if match:
        cuit_remitente = match.group().strip().replace("CUIT ", "").replace("Hora", "")
        return cuit_remitente
    else:
        pattern = r"curr\s+(\S+.*)(?=\n)"
        match = re.search(pattern, text)
        if match:
            cuit_remitente = match.group().strip().replace("curr ", "").replace(" Hora", "")
            return cuit_remitente

def get_fecha_from_text(text):
    pattern = r"\d{2}/\d{2}/\d{4}"
    match = re.search(pattern, text)
    if match:
        fecha = match.group().strip()
        return fecha

def get_importe_from_text(text):
    pattern = r"Importe\s+(\S+.*)(?=\n)"
    match = re.search(pattern, text)
    if match:
        importe = match.group().strip().replace("Importe $ ", "")
        return importe
    else:
        pattern = r"Importe\s+(\S+.*)"
        match = re.search(pattern, text)
        if match:
            importe = match.group().strip().replace("Importe ", "")
            return importe

# nombre
# importe
# fecha
# coelsa ID(solo lo tiene mercadopago)
# cuit del remitente
# cuit del destinatario