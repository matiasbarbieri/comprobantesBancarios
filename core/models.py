from django.db import models

# Create your models here.

class Comprobante(models.Model):
    archivo = models.FileField(upload_to='core/comprobantes_subidos')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_subida']

    def __str__(self):
        return str(self.fecha_subida)

    