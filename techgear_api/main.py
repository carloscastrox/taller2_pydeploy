from fastapi import FastAPI, HTTPException
from typing import List
from bson import ObjectId
from models import ProductoBase, ProductoOut, PedidoBase, PedidoOut
from database import productos_collection, pedidos_collection


app = FastAPI(
    title="TechGear API",
    description="API para el sistema de catálogo y pedidos",
    version="1.0.0",
)


# --- FUNCIONES DE AYUDA ---
def parse_producto(producto: dict) -> dict:
  return {
      "id": str(producto["_id"]),
      "nombre": producto["nombre"],
      "descripcion": producto["descripcion"],
      "precio": producto["precio"],
      "stock": producto["stock"],
      "imagen": producto.get(
          "imagen", ""
      ),  # Extrae la imagen de la BD (o cadena vacía si no existe)
  }


@app.get("/", tags=["Mensaje TechGear API"])
def home():
    return {
        "message": "Bienvenido a la API TechGear. Visita /docs para ver la documentación interactiva."
    }


# --- ENDPOINTS DE PRODUCTOS (Clase 2) ---
@app.post("/productos/", response_model=ProductoOut, tags=["Productos"])
async def crear_producto(producto: ProductoBase):
    # Insertar el producto como un diccionario
    nuevo_producto = await productos_collection.insert_one(producto.model_dump())
    # Buscar el producto recién creado
    producto_creado = await productos_collection.find_one(
        {"_id": nuevo_producto.inserted_id}
    )
    return parse_producto(producto_creado)


@app.get("/productos/", response_model=List[ProductoOut], tags=["Productos"])
async def listar_productos():
    productos = []
    async for producto in productos_collection.find():
        productos.append(parse_producto(producto))
    return productos

# --- ENDPOINT PARA OBTENER UN PRODUCTO POR ID ---
@app.get("/productos/{producto_id}", response_model=ProductoOut, tags=["Productos"])
async def obtener_producto(producto_id: str):
  # 1. Verificar que el formato del ID sea válido
  if not ObjectId.is_valid(producto_id):
    raise HTTPException(status_code=400, detail="ID de producto inválido")

  # 2. Buscar el producto en la base de datos
  producto = await productos_collection.find_one({"_id": ObjectId(producto_id)})
  if not producto:
    raise HTTPException(status_code=404, detail="Producto no encontrado")

  # 3. Retornar el producto procesado con la función de ayuda
  return parse_producto(producto) 

# ---ENDPOINTS PUT & DELELTE ---
@app.put("/productos/{producto_id}", response_model=ProductoOut, tags=["Productos"])
async def actualizar_producto(producto_id: str, producto_actualizado: ProductoBase):
    # 1. Verificar que el formato del ID sea válido
    if not ObjectId.is_valid(producto_id):
        raise HTTPException(status_code=400, detail="ID de producto inválido")

    # 2. Actualizar el documento en MongoDB usando $set
    resultado = await productos_collection.update_one(
        {"_id": ObjectId(producto_id)}, {"$set": producto_actualizado.model_dump()}
    )

    # 3. Verificar si el producto existía y fue modificado
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # 4. Obtener el producto actualizado para retornarlo
    producto = await productos_collection.find_one({"_id": ObjectId(producto_id)})
    return parse_producto(producto)


@app.delete("/productos/{producto_id}", tags=["Productos"])
async def eliminar_producto(producto_id: str):
    # 1. Verificar que el formato del ID sea válido
    if not ObjectId.is_valid(producto_id):
        raise HTTPException(status_code=400, detail="ID de producto inválido")

    # 2. Eliminar el documento de MongoDB
    resultado = await productos_collection.delete_one({"_id": ObjectId(producto_id)})

    # 3. Verificar si el producto realmente existía
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return {"message": "Producto eliminado exitosamente"}


# --- ENDPOINTS DE PEDIDOS (Clase 2) ---
@app.post("/pedidos/", response_model=PedidoOut, tags=["Pedidos"])
async def crear_pedido(pedido: PedidoBase):
    # 1. Verificar que el formato del ID sea válido
    if not ObjectId.is_valid(pedido.producto_id):
        raise HTTPException(status_code=400, detail="ID de producto inválido")

    # 2. Buscar si el producto existe
    producto = await productos_collection.find_one(
        {"_id": ObjectId(pedido.producto_id)}
    )
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # 3. Validar el stock
    if producto["stock"] < pedido.cantidad:
        raise HTTPException(
            status_code=400, detail="Stock insuficiente para realizar el pedido"
        )

    # 4. Calcular el total del pedido
    total = producto["precio"] * pedido.cantidad

    # 5. Insertar el pedido en la base de datos
    nuevo_pedido = {
        "producto_id": pedido.producto_id,
        "cantidad": pedido.cantidad,
        "total": total,
    }
    resultado = await pedidos_collection.insert_one(nuevo_pedido)

    # 6. Actualizar (descontar) el stock del producto
    await productos_collection.update_one(
        {"_id": ObjectId(pedido.producto_id)},
        {"$set": {"stock": producto["stock"] - pedido.cantidad}},
    )

    return {
        "id": str(resultado.inserted_id),
        "producto_id": pedido.producto_id,
        "cantidad": pedido.cantidad,
        "total": total,
    }
    
@app.get("/pedidos/", tags=["Pedidos"])
async def listar_pedidos():
  pedidos = []
  async for pedido in pedidos_collection.find():
    # Buscar el producto relacionado para inyectar su nombre en el detalle
    producto = await productos_collection.find_one(
        {"_id": ObjectId(pedido["producto_id"])}
    )
    nombre_producto = producto["nombre"] if producto else "Producto no encontrado"

    pedidos.append({
        "id": str(pedido["_id"]),
        "producto_id": pedido["producto_id"],
        "nombre_producto": nombre_producto,  # 👈 Nuevo campo detallado
        "cantidad": pedido["cantidad"],
        "total": pedido["total"],
    })
  return pedidos      