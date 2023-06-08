from django.db import models

# Create your models here.

class Comprobante(models.Model):
    archivo = models.FileField(upload_to='core/comprobantes_subidos', null=True, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    operacion = models.IntegerField(unique=True, null=True, blank=True)
    operacion_multiple_uid = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['-fecha_subida']

    def __str__(self):
        return str(self.fecha_subida)

    