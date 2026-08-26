from django.shortcuts import redirect
from django.urls import path
from . import views

urlpatterns = [
    # Rutas para el Catálogo Público
    path("", views.catalogo, name="catalogo"),
    # Rutas para la Gestión de Productos
    path("admon/", views.admon_productos, name="admon_productos"),
    # Agregadas estas rutas que faltaban y rompían el HTML
    path(
        "admon/editar/<str:producto_id>/",
        views.editar_producto,
        name="editar_producto",
    ),
    path(
        "admon/eliminar/<str:producto_id>/",
        views.eliminar_producto,
        name="eliminar_producto",
    ),
    # Rutas para Pedidos
    path("pedido/<str:producto_id>/", views.realizar_pedido, name="realizar_pedido"),
    path("pedidos/", views.pedidos, name="pedidos"),
    # Ruta para la documentación de la API (Swagger)
    path(
        "swagger/",
        lambda request: redirect("http://127.0.0.1:8001/docs"),
        name="api_swagger",
    ),
]