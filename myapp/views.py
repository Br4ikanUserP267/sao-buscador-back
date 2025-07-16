from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.pagination import PageNumberPagination

from django.db.models import Q, Value, IntegerField, Case, When
from .models import Producto
from .serializers import ProductoSerializer

class ProductoPagination(PageNumberPagination):
    page_size = 10  # ✔️ 10 productos por página
    page_size_query_param = 'page_size'
    max_page_size = 50


class BusquedaProductoAPIView(APIView):
    renderer_classes = [JSONRenderer]


    def get(self, request):
        q = request.GET.get('q', '').strip().lower()
        if not q:
            return Response({"results": [], "count": 0})

        productos = Producto.objects.annotate(
            prioridad=Case(
                When(descripcion__istartswith=q, then=Value(1)),
                When(descripcion__icontains=q, then=Value(2)),
                When(keyword__istartswith=q, then=Value(3)),
                When(keyword__icontains=q, then=Value(4)),
                When(palabras_clave__palabra__istartswith=q, then=Value(5)),
                When(palabras_clave__palabra__icontains=q, then=Value(6)),
                default=Value(99),
                output_field=IntegerField()
            )
        ).filter(
            Q(descripcion__icontains=q) |
            Q(sku_ean__icontains=q) |
            Q(plusicol__icontains=q) |
            Q(departamento__icontains=q) |
            Q(subcategoria__icontains=q) |
            Q(tipo__icontains=q) |
            Q(keyword__icontains=q) |
            Q(palabras_clave__palabra__icontains=q)
        ).distinct().order_by('prioridad')

        paginator = ProductoPagination()
        result_page = paginator.paginate_queryset(productos, request)
        serializer = ProductoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class ListaPalabrasClaveAPIView(APIView):
    def get(self, request):
        palabras = (
            Producto.objects.exclude(keyword__isnull=True)
            .exclude(keyword__exact="")
            .values_list("keyword", flat=True)
            .distinct()
        )
        # Convertir cada string en una lista de palabras, limpiando espacios
        resultado = [list(map(str.strip, palabra.split(","))) for palabra in palabras if palabra]
        return Response(resultado)