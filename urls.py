from django.contrib import admin
from django.urls import path
from .views import index, derivadas_parciales_view, transformada_laplace_view, optimizacion_funciones_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('derivadas_parciales/', derivadas_parciales_view, name='derivadas_parciales'),
    path('transformada_laplace/', transformada_laplace_view, name='transformada_laplace'),
    path('optimizacion_funciones/', optimizacion_funciones_view, name='optimizacion_funciones'),
]

