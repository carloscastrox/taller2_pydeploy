import os
import requests
from django.shortcuts import redirect, render

# Si existe una variable de entorno en Vercel la usa; si no, usa localhost para desarrollo local

#FASTAPI_URL = os.environ.get(
#    "FASTAPI_URL", "http://127.0.0.1:8001"
#)

FASTAPI_URL = os.getenv("FASTAPI_URL", "https://taller2-pydeploy.onrender.com")
url = f"{FASTAPI_URL}/TU_ENDPOINT" 

def catalogo(request):  # Vista exclusiva para el Catálogo Público
  try:
    response = requests.get(f"{FASTAPI_URL}/productos/")
    productos = response.json() if response.status_code == 200 else []
  except requests.exceptions.RequestException:
    productos = []
  return render(request, "catalogo.html", {"productos": productos})

def admon_productos(request):
  try:
    response = requests.get(f"{FASTAPI_URL}/productos/")
    productos = response.json() if response.status_code == 200 else []
  except requests.exceptions.RequestException:
    productos = []
  return render(request, "admon_productos.html", {"productos": productos})

def eliminar_producto(request, producto_id):
  """Envía una petición DELETE a FastAPI para eliminar el producto."""
  try:
    requests.delete(f"{FASTAPI_URL}/productos/{producto_id}")
  except requests.exceptions.RequestException:
    pass
  return redirect("admon_productos")


def editar_producto(request, producto_id):
  """Obtiene los datos del producto para mostrarlos y procesa la actualización vía PUT."""
  producto = {}

  # 1. Obtener los datos actuales del producto desde FastAPI para rellenar el formulario
  try:
    response_get = requests.get(f"{FASTAPI_URL}/productos/{producto_id}")
    if response_get.status_code == 200:
      producto = response_get.json()
  except requests.exceptions.RequestException:
    pass

  # 2. Si el usuario envía el formulario con los cambios (POST / PUT)
  if request.method == "POST":
    nombre = request.POST.get("nombre")
    descripcion = request.POST.get("descripcion")
    precio = request.POST.get("precio")
    stock = request.POST.get("stock")
    imagen = request.POST.get("imagen", "")

    datos_actualizados = {
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": float(precio),
        "stock": int(stock),
        "imagen": imagen,
    }

    try:
      response_put = requests.put(
          f"{FASTAPI_URL}/productos/{producto_id}", json=datos_actualizados
      )
      if response_put.status_code == 200:
        return redirect("admon_productos")
    except requests.exceptions.RequestException:
      pass

  return render(
      request,
      "admon_producto.html",
      {"producto": producto, "producto_id": producto_id},
  )


def realizar_pedido(request, producto_id):
  # 1. Consultar los detalles del producto en FastAPI
  producto = {}
  try:
    response_prod = requests.get(f"{FASTAPI_URL}/productos/{producto_id}")
    if response_prod.status_code == 200:
      producto = response_prod.json()
  except requests.exceptions.RequestException:
    pass

  # 2. Procesar el formulario cuando se envía (POST)
  if request.method == "POST":
    cantidad = request.POST.get("cantidad", 1)
    try:
      response_pedido = requests.post(
          f"{FASTAPI_URL}/pedidos/",
          json={"producto_id": producto_id, "cantidad": int(cantidad)},
      )
      if response_pedido.status_code in [200, 201]:
        return redirect(
            "catalogo"
        )  # O 'catalogo_productos' según cómo lo tengas en tu urls.py
    except requests.exceptions.RequestException:
      pass

  # 3. Renderizar el template enviando tanto el producto como el ID
  return render(
      request,
      "checkout.html",
      {
          "producto_id": producto_id,
          "producto": producto,
      },
  )

def pedidos(request):
  try:
    response = requests.get(f"{FASTAPI_URL}/pedidos/")
    pedidos = response.json() if response.status_code == 200 else []
  except requests.exceptions.RequestException:
    pedidos = []
  return render(request, "pedidos.html", {"pedidos": pedidos})
