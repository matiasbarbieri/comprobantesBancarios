from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name="upload_file"),
    # path('upload_file/', views.upload_file, name="upload_file"),
    # path('list/', views.upload_file, name='list'),
    # path('comprobantes/<int:comprobante_id>', views.procesar_comprobante, name="procesar_comprobante"),
    path('comprobantes/<int:operacion>', views.procesar_comprobante, name="procesar_comprobante"),
    path('comprobantes/multiple/<int:operacion_multiple_uid>/', views.procesar_comprobante_multiple, name="procesar_comprobante_multiple"),
]