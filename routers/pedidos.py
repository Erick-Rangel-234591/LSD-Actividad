from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd

router = APIRouter()

usuarios_db = [
    {"id": 1, "name": "Admin User"},
    {"id": 2, "name": "Cliente User"}
]

carritos_db = [
    {"usuario_id": 1, "items": [{"producto_id": 1, "cantidad": 2}]},
    {"usuario_id": 2, "items": [{"producto_id": 2, "cantidad": 1}]}
]

productos_db = {
    1: {"nombre": "Laptop Corporativa", "precio": 25000.0},
    2: {"nombre": "Silla Ejecutiva", "precio": 4500.0},
    3: {"nombre": "Mouse Inalámbrico", "precio": 600.0}
}

pedidos_db = []

plantilla_factura_2019 = """
<html>
<head><title>Factura Amazonas 2019</title></head>
<body>
<h1>Factura de Compra</h1>
<p>Gracias por tu compra en Amazonas.</p>
<table>
<tr><th>Producto</th><th>Cantidad</th><th>Precio</th></tr>
<tr><td>Laptop Corporativa</td><td>1</td><td>25000</td></tr>
<tr><td>Silla Ejecutiva</td><td>1</td><td>4500</td></tr>
</table>
<p>Total: 29500</p>
</body>
</html>
"""

class PedidoCreate(BaseModel):
    usuario_id: int
    envio: float

class PedidoEstado(BaseModel):
    pedido_id: int
    estado: str


def calcular_total(subtotal: float, envio: float):
    total = subtotal + envio
    iva = total * 0.16
    df = pd.DataFrame([{"subtotal": subtotal, "envio": envio, "iva": iva, "total": total + iva}])
    return float(df["total"].sum())


def obtener_carrito(usuario_id: int):
    for carrito in carritos_db:
        if carrito["usuario_id"] == usuario_id:
            return carrito
    return {"usuario_id": usuario_id, "items": []}


def calcular_subtotal_carrito(carrito: dict):
    subtotal = 0.0
    for item in carrito["items"]:
        producto = productos_db.get(item["producto_id"])
        if producto:
            subtotal += producto["precio"] * item["cantidad"]
    return subtotal


@router.post("/pedidos/crear")
def crear_pedido(datos: PedidoCreate):
    carrito = obtener_carrito(datos.usuario_id)
    subtotal = calcular_subtotal_carrito(carrito)
    total = calcular_total(subtotal, datos.envio)
    pedido_id = len(pedidos_db) + 1
    pedido = {
        "pedido_id": pedido_id,
        "usuario_id": datos.usuario_id,
        "subtotal": subtotal,
        "envio": datos.envio,
        "total": total,
        "estado": "Pendiente",
        "items": carrito["items"]
    }
    pedidos_db.append(pedido)
    # [Bug - Flujo]: no vacía el carrito original
    return pedido


@router.patch("/pedidos/estado")
def cambiar_estado(patch: PedidoEstado):
    pedido = next((p for p in pedidos_db if p["pedido_id"] == patch.pedido_id), None)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    # [Bug - Estados]: permite cambiar de Cancelado a Enviado sin validación
    pedido["estado"] = patch.estado
    return pedido


@router.get("/pedidos/simular_cripto")
def simular_cripto():
    base = 100.0
    tasa = 1.13
    return {"monto_cripto": base * tasa, "tasa": tasa}
