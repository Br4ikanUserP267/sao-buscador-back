from django.db import models

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    sku_ean = models.CharField(max_length=20, null=True, blank=True)
    plusicol = models.IntegerField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    keyword = models.TextField(null=True, blank=True)
    departamento = models.CharField(max_length=100, null=True, blank=True)
    subcategoria = models.CharField(max_length=100, null=True, blank=True)
    tipo = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'productos'
        managed = False

class PalabraClave(models.Model):
    palabra = models.CharField(max_length=200)
    producto = models.ForeignKey(Producto, related_name="palabras_clave", on_delete=models.CASCADE)

    class Meta:
        db_table = 'palabras_clave'  # No pongas managed=False aquí
