from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('upload_file/', views.upload_file, name="upload_file"),
    path('comprobantes/<int:comprobante_id>', views.procesar_comprobante, name="procesar_comprobante"),   
]