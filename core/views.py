from django.shortcuts import render, HttpResponse, redirect
from .banks import bancos, bbva, macro, nacion, santander, santander2, mercadopago, naranjax, brubank, lemon, icbc, galicia, ciudad
from django.http import JsonResponse
import os
import uuid
from .models import Comprobante
from .forms import UploadFileForm
from .banks.bancos import get_banco_del_comprobante
# Create your views here.

def home(request):
    return render(request, 'core/home.html')


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        file_list = []
        operacion_multiple_uid = uuid.uuid4().int & (1<<32)-1  # UUID único para la operación múltiple

        for f in request.FILES.getlist('file'):
            operacion_uuid = uuid.uuid4().int & (1<<32)-1
            comprobante = Comprobante(archivo=f)
            file_list.append(comprobante)
            comprobante.operacion = operacion_uuid
            comprobante.operacion_multiple_uid = operacion_multiple_uid
            comprobante.save()
        
        if len(file_list) == 1:
            return redirect('procesar_comprobante', operacion=comprobante.operacion)
        if len(file_list) > 1:
            return redirect('procesar_comprobante_multiple', operacion_multiple_uid=operacion_multiple_uid)
        else:
            return HttpResponse('Error: operacion es None')

        return HttpResponse("Los archivos se subieron correctamente")
    else: # GET
        form = UploadFileForm()
    return render(request, 'core/home.html', {'form': form})    # el form es el formulario que se muestra en la pagina 

def procesar_comprobante(request, operacion):
    comprobante = Comprobante.objects.get(operacion=operacion) # Obtener el comprobante que se subió
    pdf_path = comprobante.archivo.path # Obtener el path del archivo subido para luego pasarlo a la funcion get_banco_del_comprobante

    banco_del_comprobante = get_banco_del_comprobante(pdf_path) # Aca se llama a la funcion que se encuentra en el archivo bancos.py
    
    if banco_del_comprobante:
        # Se encontró un banco válido, ejecutar las funciones restantes del archivo
        titular = banco_del_comprobante['titular']
        banco = banco_del_comprobante['banco']
        cuit_remitente = banco_del_comprobante['cuit_remitente']
        fecha = banco_del_comprobante['fecha']
        importe = banco_del_comprobante['importe']

        # Construir el diccionario de contexto con los datos obtenidos
        context = {
            'titular': titular,
            'banco': banco,
            'cuit_remitente': cuit_remitente,
            'fecha': fecha,
            'importe': importe
        }
        
        return JsonResponse(context)
    else:
        return render(request, 'core/error.html')
    

def procesar_comprobante_multiple(request, operacion_multiple_uid):
    comprobantes = Comprobante.objects.filter(operacion_multiple_uid=operacion_multiple_uid)  # Obtener todos los comprobantes con el mismo UID de operación múltiple
    print(comprobantes)
    if comprobantes:
        context = {'comprobantes': []}

        for comprobante in comprobantes:
            pdf_path = comprobante.archivo.path
            banco_del_comprobante = get_banco_del_comprobante(pdf_path)

            if banco_del_comprobante:
                # Se encontró un banco válido, ejecutar las funciones restantes del archivo
                titular = banco_del_comprobante['titular']
                banco = banco_del_comprobante['banco']
                cuit_remitente = banco_del_comprobante['cuit_remitente']
                fecha = banco_del_comprobante['fecha']
                importe = banco_del_comprobante['importe']

                # Construir el diccionario de contexto con los datos obtenidos
                context['comprobantes'].append({
                    'titular': titular,
                    'banco': banco,
                    'cuit_remitente': cuit_remitente,
                    'fecha': fecha,
                    'importe': importe
                })
        return JsonResponse(context)
    else:
        return render(request, 'core/error.html')
            







# def upload_file(request):
#     if request.method == 'POST' and request.FILES['file']:
#         file = request.FILES['file']

#         comprobante = Comprobante(archivo=file)
#         comprobante.operacion = uuid.uuid4().int & (1<<32)-1
#         comprobante.save()

#         # return redirect('procesar_comprobante', comprobante_id=comprobante.id)
#         if comprobante.operacion is not None:
#             return redirect('procesar_comprobante', operacion=comprobante.operacion)
#         else:
#             # Manejar el caso cuando el campo operacion es None
#             return HttpResponse('Error: operacion es None')

#     return HttpResponse('No se subió ningún archivo')







# def procesar_comprobante(request, comprobante_id):
#     comprobante = Comprobante.objects.get(id=comprobante_id)
#     pdf_path = comprobante.archivo.path

#     # banco_del_comprobante = bbva.get_banco_from_text(bbva.get_text_from_pdf(pdf_path))
#     banco_del_comprobante = get_banco_del_comprobante(pdf_path)
    
#     if banco_del_comprobante:
#         # Se encontró un banco válido, ejecutar las funciones restantes del archivo
#         titular = banco_del_comprobante['titular']
#         banco = banco_del_comprobante['banco']
#         cuit_remitente = banco_del_comprobante['cuit_remitente']
#         fecha = banco_del_comprobante['fecha']
#         importe = banco_del_comprobante['importe']

#         # Construir el diccionario de contexto con los datos obtenidos
#         context = {
#             'titular': titular,
#             'banco': banco,
#             'cuit_remitente': cuit_remitente,
#             'fecha': fecha,
#             'importe': importe
#         }
        
#         return JsonResponse(context)
#     else:
#         return render(request, 'core/error.html')
    
























# def home(request):
#     return render(request, 'core/home.html')

# def procesar_comprobante(request):
#     banco_bbva = 'banco bbva'
#     banco_macro = 'banco macro'
#     banco_nacion = 'banco nacion'
#     banco_santander = 'banco santander rio'
#     banco_mp = 'mercado pago'
#     banco_naranjax = 'naranja x'
#     banco_brubank = 'brubank'
#     banco_lemon = 'lemon'
#     banco_icbc = 'icbc'
#     banco_galicia = 'galicia'
#     banco_ciudad = 'ciudad'

#     banco_del_comprobante = banco_icbc

#     if banco_del_comprobante == banco_bbva:
#         # pdf_path = 'comprobantes/bbva/bbvatransfer.pdf'
#         pdf_path = 'core/comprobantes/bbva/bbva.jpg'
#         # pdf_path = 'comprobantes/bbva/file.pdf'
#         titular = bbva.get_titular_from_text(bbva.get_text_from_pdf(pdf_path))
#         banco = bbva.get_banco_from_text(bbva.get_text_from_pdf(pdf_path))
#         cuit_remitente = bbva.get_cuit_remitente_from_text(bbva.get_text_from_pdf(pdf_path))
#         fecha = bbva.get_fecha_from_text(bbva.get_text_from_pdf(pdf_path))
#         importe = bbva.get_importe_from_text(bbva.get_text_from_pdf(pdf_path))

#     if banco_del_comprobante == banco_macro:
#         bcomacro = 'core/comprobantes/macro/macro.jpg'
#         titular = macro.get_titular_from_text(macro.get_text_from_pdf(bcomacro))
#         banco = macro.get_banco_from_text(macro.get_text_from_pdf(bcomacro))
#         cuit_remitente = macro.get_cuit_remitente_from_text(macro.get_text_from_pdf(bcomacro))
#         fecha = macro.get_fecha_from_text(macro.get_text_from_pdf(bcomacro))
#         importe = macro.get_importe_from_text(macro.get_text_from_pdf(bcomacro))
    
#     if banco_del_comprobante == banco_nacion:
#         bconacion = 'core/comprobantes/nacion/Banco_Nacion.jpg'
#         titular = nacion.get_titular_from_text(nacion.get_text_from_pdf(bconacion))
#         banco = nacion.get_banco_from_text(nacion.get_text_from_pdf(bconacion))
#         cuit_remitente = nacion.get_cuit_remitente_from_text(nacion.get_text_from_pdf(bconacion))
#         fecha = nacion.get_fecha_from_text(nacion.get_text_from_pdf(bconacion))
#         importe = nacion.get_importe_from_text(nacion.get_text_from_pdf(bconacion))
    
#     if banco_del_comprobante == banco_santander:
#         bcosantander = 'core/comprobantes/santander/santander.jpg'
#         titular = santander.get_titular_from_text(santander.get_text_from_pdf(bcosantander))
#         banco = santander.get_banco_from_text(santander.get_text_from_pdf(bcosantander))
#         cuit_remitente = santander.get_cuit_remitente_from_text(santander.get_text_from_pdf(bcosantander))
#         fecha = santander.get_fecha_from_text(santander.get_text_from_pdf(bcosantander))
#         importe = santander.get_importe_from_text(santander.get_text_from_pdf(bcosantander))

#     if banco_del_comprobante == banco_santander:
#         bcosantander = 'core/comprobantes/santander/santander2.jpg'
#         titular = santander2.get_titular_from_text(santander2.get_text_from_pdf(bcosantander))
#         banco = santander2.get_banco_from_text(santander2.get_text_from_pdf(bcosantander))
#         cuit_remitente = santander2.get_cuit_remitente_from_text(santander2.get_text_from_pdf(bcosantander))
#         fecha = santander2.get_fecha_from_text(santander2.get_text_from_pdf(bcosantander))
#         importe = santander2.get_importe_from_text(santander2.get_text_from_pdf(bcosantander))

#     if banco_del_comprobante == banco_mp:
#         mp = 'core/comprobantes/mercadopago/mercadopago-1.pdf'
#         # mp = 'comprobantes/mercadopago/MPIMAGEN.jpg'
#         titular = mercadopago.get_titular_from_text(mercadopago.get_text_from_pdf(mp))
#         banco = mercadopago.get_banco_from_text(mercadopago.get_text_from_pdf(mp))
#         cuit_remitente = mercadopago.get_cuit_remitente_from_text(mercadopago.get_text_from_pdf(mp))
#         fecha = mercadopago.get_fecha_from_text(mercadopago.get_text_from_pdf(mp))
#         importe = mercadopago.get_importe_from_text(mercadopago.get_text_from_pdf(mp))
#         coelsa = mercadopago.get_coelsa_from_text(mercadopago.get_text_from_pdf(mp))

#     if banco_del_comprobante == banco_naranjax:
#         naranja = 'core/comprobantes/naranjax/naranjax.jpg'
#         titular = naranjax.get_titular_from_text(naranjax.get_text_from_pdf(naranja))
#         banco = naranjax.get_banco_from_text(naranjax.get_text_from_pdf(naranja))
#         cuit_remitente = naranjax.get_cuit_remitente_from_text(naranjax.get_text_from_pdf(naranja))
#         fecha = naranjax.get_fecha_from_text(naranjax.get_text_from_pdf(naranja))
#         importe = naranjax.get_importe_from_text(naranjax.get_text_from_pdf(naranja))

#     if banco_del_comprobante == banco_brubank:
#         # bcobrubank = 'comprobantes/brubank/brubank.jpg' #TODO no funciona
#         bcobrubank = 'core/comprobantes/brubank/brubank2.jpg'
#         titular = brubank.get_titular_from_text(brubank.get_text_from_pdf(bcobrubank))
#         banco = brubank.get_banco_from_text(brubank.get_text_from_pdf(bcobrubank))
#         cuit_remitente = brubank.get_cuit_remitente_from_text(brubank.get_text_from_pdf(bcobrubank))
#         fecha = brubank.get_fecha_from_text(brubank.get_text_from_pdf(bcobrubank))
#         importe = brubank.get_importe_from_text(brubank.get_text_from_pdf(bcobrubank))

#     if banco_del_comprobante == banco_lemon:
#         bcolemon = 'core/comprobantes/lemon/lemon.jpg'
#         titular = lemon.get_titular_from_text(lemon.get_text_from_pdf(bcolemon))
#         banco = lemon.get_banco_from_text(lemon.get_text_from_pdf(bcolemon))
#         cuit_remitente = lemon.get_cuit_remitente_from_text(lemon.get_text_from_pdf(bcolemon))
#         fecha = lemon.get_fecha_from_text(lemon.get_text_from_pdf(bcolemon))
#         importe = lemon.get_importe_from_text(lemon.get_text_from_pdf(bcolemon))

#     if banco_del_comprobante == banco_icbc:
#         bcoicbc = 'core/comprobantes/icbc/icbc.jpg'
#         titular = icbc.get_titular_from_text(icbc.get_text_from_pdf(bcoicbc))
#         banco = icbc.get_banco_from_text(icbc.get_text_from_pdf(bcoicbc))
#         cuit_remitente = icbc.get_cuit_remitente_from_text(icbc.get_text_from_pdf(bcoicbc))
#         fecha = icbc.get_fecha_from_text(icbc.get_text_from_pdf(bcoicbc))
#         importe = icbc.get_importe_from_text(icbc.get_text_from_pdf(bcoicbc))

#     if banco_del_comprobante == banco_galicia:
#         bcogalicia = 'core/comprobantes/galicia/galicia.jpg'
#         titular = galicia.get_titular_from_text(galicia.get_text_from_pdf(bcogalicia))
#         banco = galicia.get_banco_from_text(galicia.get_text_from_pdf(bcogalicia))
#         cuit_remitente = galicia.get_cuit_remitente_from_text(galicia.get_text_from_pdf(bcogalicia))
#         fecha = galicia.get_fecha_from_text(galicia.get_text_from_pdf(bcogalicia))
#         importe = galicia.get_importe_from_text(galicia.get_text_from_pdf(bcogalicia))
    
#     if banco_del_comprobante == banco_ciudad:
#         bcociudad = 'core/comprobantes/ciudad/bancociudad.jpg'
#         titular = ciudad.get_titular_from_text(ciudad.get_text_from_pdf(bcociudad))
#         banco = ciudad.get_banco_from_text(ciudad.get_text_from_pdf(bcociudad))
#         cuit_remitente = ciudad.get_cuit_remitente_from_text(ciudad.get_text_from_pdf(bcociudad))
#         fecha = ciudad.get_fecha_from_text(ciudad.get_text_from_pdf(bcociudad))
#         importe = ciudad.get_importe_from_text(ciudad.get_text_from_pdf(bcociudad))


#     if banco:
#         # Haz lo que necesites con los datos obtenidos del comprobante
        
#         #paso los datos obtenidos a la vista con un diccionario de contexto
#         context = {
#             'nombre': titular,
#             'banco': banco,
#             'cuit_remitente': cuit_remitente,
#             'fecha': fecha,
#             'importe': importe
#         }
#         return JsonResponse(context)
#         # return render(request, 'core/resultado.html', context)
#     else:
#         return render(request, 'core/error.html')