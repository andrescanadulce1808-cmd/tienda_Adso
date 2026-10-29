from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, Field, EmailStr

# EmailStr necesita email-validator, incluido por fastapi[standard] en instalaciones habituales.
class ClienteCrear(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    correo: EmailStr

class ClienteRespuesta(ClienteCrear):
    id: int

class ProductoCrear(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    precio: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    stock: int = Field(ge=0)

class ProductoRespuesta(ProductoCrear):
    id: int

class ItemPedido(BaseModel):
    producto_id: int = Field(gt=0)
    cantidad: int = Field(gt=0)

class PedidoCrear(BaseModel):
    cliente_id: int = Field(gt=0)
    items: list[ItemPedido] = Field(min_length=1)
    # Estado inicial opcional (Reto B). Por defecto el pedido nace confirmado.
    estado: Literal['pendiente', 'confirmado'] = 'confirmado'

class EstadoCambiar(BaseModel):
    estado: Literal['pendiente', 'confirmado', 'cancelado']