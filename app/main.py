from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo de datos
class Producto(BaseModel):
    id: int | None = None
    nombre: str
    precio: float
    stock: int

# Simulación de Base de Datos en memoria
db_productos: List[Producto] = [
    Producto(id=1, nombre="Cuaderno SENA", precio=5500.0, stock=20),
    Producto(id=2, nombre="Esfero Negro", precio=1200.0, stock=50)
]

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

# --- ENDPOINTS API ---

@app.get("/productos", response_model=List[Producto])
def get_productos():
    return db_productos

@app.post("/productos", response_model=Producto)
def create_producto(prod: Producto):
    prod.id = len(db_productos) + 1
    db_productos.append(prod)
    return prod

@app.delete("/productos/{prod_id}")
def delete_producto(prod_id: int):
    global db_productos
    db_productos = [p for p in db_productos if p.id != prod_id]
    return {"message": "Producto eliminado"}