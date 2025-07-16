# searcher/urls.py
from django.contrib import admin
from django.urls import path
from myapp.views import BusquedaProductoAPIView, ListaPalabrasClaveAPIView

urlpatterns = [
    path("palabras-clave/", ListaPalabrasClaveAPIView.as_view()),
    path("buscar-producto/", BusquedaProductoAPIView.as_view()),
]