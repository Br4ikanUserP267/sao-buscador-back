from rest_framework import serializers
from .models import Producto, PalabraClave

class PalabraClaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalabraClave
        fields = ['palabra']

class ProductoSerializer(serializers.ModelSerializer):
    palabras_clave = PalabraClaveSerializer(many=True, read_only=True)

    class Meta:
        model = Producto
        fields = [
            'id', 'sku_ean', 'plusicol', 'descripcion',
            'departamento', 'subcategoria', 'tipo',
            'keyword', 'palabras_clave'
        ]
