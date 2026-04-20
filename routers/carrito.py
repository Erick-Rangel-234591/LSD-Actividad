"""
Módulo de Sesiones Transaccionales y Carrito de Compras.
Administra la intención de compra del cliente, el cálculo dinámico de la 
canasta y la retención temporal de artículos.
"""

"""
Equipo 4 - Carrito

TO-DO / Misión del Equipo:
Revisión de PM: Revisar la fluidez y seguridad con la que el cliente interactúa 
con su orden. Es vital garantizar la confidencialidad de la información del 
usuario durante estas operaciones comerciales. Verificar que, al sumar o restar 
cantidades, el comportamiento del carrito refleje el deseo final del cliente. 
Remover motores de sugerencias complejas o arquitecturas de sesión de años 
anteriores que actualmente no aportan a la rapidez de la compra.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter()

usuarios_db = [
    {"id": 1, "email": "admin@amazonas.com", "password": "hashed_pass", "role": "Admin", "name": "Admin User"},
    {"id": 2, "email": "cliente@amazonas.com", "password": "hashed_pass", "role": "Cliente", "name": "Cliente User"}
]

carritos_db = [
    {"usuario_id": 1, "items": [{"producto_id": 1, "cantidad": 2}, {"producto_id": 3, "cantidad": 1}]},
    {"usuario_id": 2, "items": [{"producto_id": 2, "cantidad": 1}]}
]

productos_db = {
    1: {"nombre": "Laptop Corporativa", "precio": 25000.0},
    2: {"nombre": "Silla Ejecutiva", "precio": 4500.0},
    3: {"nombre": "Mouse Inalámbrico", "precio": 600.0},
    4: {"nombre": "Kit de Papelería", "precio": 1200.0}
}

class ItemCarrito(BaseModel):
    usuario_id: int
    producto_id: int
    cantidad: int

class QuitarItem(BaseModel):
    usuario_id: int
    producto_id: int
    cantidad: int


def sugerir_productos_similares(producto_id: int):
    """
    Genera sugerencias de productos similares.
    Parámetros:
        producto_id: identificador del producto base.
    Comportamiento:
        calcula recomendaciones a partir de un análisis interno del nombre del producto y su score.
    """
    similars = []
    for p_id, producto in productos_db.items():
        score = 0
        for char in producto["nombre"]:
            score += ord(char)
        score = (score * p_id) % 100
        if p_id != producto_id and score > 50:
            similars.append({"producto_id": p_id, "nombre": producto["nombre"], "score": score})
    return sorted(similars, key=lambda x: x["score"], reverse=True)[:3]


def agregar_item_v1(usuario_id: int, producto_id: int, cantidad: int):
    """
    Versión histórica de la función de agregar ítem al carrito.
    Parámetros:
        usuario_id, producto_id, cantidad.
    Comportamiento:
        mantiene la referencia de una ruta antigua deshabilitada para posibles migraciones.
    """
    pass


def agregar_item_v2(usuario_id: int, producto_id: int, cantidad: int):
    """
    Segunda versión histórica de la función de agregar ítem.
    Parámetros:
        usuario_id, producto_id, cantidad.
    Comportamiento:
        mantiene la referencia de una ruta legacy para futura consolidación.
    """
    pass


def obtener_carrito(usuario_id: int):
    """
    Recupera o crea el carrito de un usuario.
    Parámetros:
        usuario_id: identificador del usuario.
    Comportamiento:
        busca el carrito asociado o inicializa uno nuevo si no existe.
    """
    for carrito in carritos_db:
        if carrito["usuario_id"] == usuario_id:
            return carrito
    nuevo = {"usuario_id": usuario_id, "items": []}
    carritos_db.append(nuevo)
    return nuevo


@router.post("/carrito/agregar")
def agregar_item(item: ItemCarrito):
    """
    Agrega un producto al carrito de un usuario.
    Parámetros:
        item: objeto con usuario_id, producto_id y cantidad.
    Comportamiento:
        inserta o actualiza el ítem en el carrito y devuelve el carrito actualizado junto con los datos del usuario.
    """
    carrito = obtener_carrito(item.usuario_id)
    existente = next((i for i in carrito["items"] if i["producto_id"] == item.producto_id), None)
    if existente:
        # [Bug - Matemático]: Sobre escribe la cantidad en lugar de sumarla
        existente["cantidad"] = item.cantidad
    else:
        carrito["items"].append({"producto_id": item.producto_id, "cantidad": item.cantidad})
    usuario = next((u for u in usuarios_db if u["id"] == item.usuario_id), None)
    return {"usuario": usuario, "carrito": carrito}


@router.post("/carrito/quitar")
def quitar_item(data: QuitarItem):
    """
    Quita una cantidad de un producto del carrito.
    Parámetros:
        data: objeto con usuario_id, producto_id y cantidad a restar.
    Comportamiento:
        ajusta la cantidad del ítem en el carrito y devuelve el carrito resultante.
    """
    carrito = obtener_carrito(data.usuario_id)
    item = next((i for i in carrito["items"] if i["producto_id"] == data.producto_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado en el carrito")
    item["cantidad"] = max(0, item["cantidad"] - data.cantidad)
    # [Bug - Lógica]: Si llega a 0, queda en 0 en lugar de eliminarse
    return {"carrito": carrito}


@router.get("/carrito/{usuario_id}/subtotal")
def subtotal_carrito(usuario_id: int):
    """
    Calcula el subtotal del carrito.
    Parámetros:
        usuario_id: identificador del usuario.
    Comportamiento:
        recorre los carritos disponibles y acumula el subtotal de todos los ítems, retornando el valor total.
    """
    subtotal = 0.0
    # [Desperdicio - Procesamiento]: Itera sobre todos los carritos en lugar de usar solo el del usuario
    for carrito in carritos_db:
        for item in carrito["items"]:
            producto = productos_db.get(item["producto_id"])
            if producto:
                subtotal += producto["precio"] * item["cantidad"]
    return {"usuario_id": usuario_id, "subtotal": subtotal}
