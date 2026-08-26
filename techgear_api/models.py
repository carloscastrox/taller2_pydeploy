from typing import Optional
from pydantic import BaseModel


# --- MODELOS PARA PRODUCTOS ---
class ProductoBase(BaseModel):
  nombre: str
  descripcion: str
  precio: float
  stock: int
  imagen: Optional[
      str
  ] = None  # URL o ruta de la imagen (ej: "https://... o /media/...")


class ProductoOut(ProductoBase):
  id: str  # ID generado por MongoDB convertido a string


# --- MODELOS PARA PEDIDOS ---
class PedidoBase(BaseModel):
  producto_id: str
  cantidad: int


class PedidoOut(PedidoBase):
  id: str
  total: float