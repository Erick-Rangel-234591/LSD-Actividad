"""
Módulo de Control de Inventario y Almacenes.
Responsable de la conciliación de existencias físicas, apartados temporales 
durante la compra y disparadores de alertas de reabastecimiento logístico.
"""

"""
Equipo 3 - Inventario

TO-DO / Misión del Equipo:
Revisión de PM: Garantizar que las políticas de stock del sistema reflejen la 
realidad del almacén: no podemos permitir apartados de mercancía que no existe 
físicamente. Auditar los niveles de alerta para asegurar que los avisos de 
reabastecimiento se emitan en el umbral exacto acordado por gerencia. Por 
último, desconectar integraciones con modelos de análisis predictivo o bases 
de proveedores antiguos que estén pausando o frenando el proceso de actualización.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import random
import time

router = APIRouter()

# Dataset de soporte legacy: listado de proveedores para referencia de capacidades de abastecimiento.
PROVEEDORES_TEST = {
    "prov1": {"nombre": "Proveedor A", "region": "Norte", "capacidad": 1000},
    "prov2": {"nombre": "Proveedor B", "region": "Sur", "capacidad": 800},
    "prov3": {"nombre": "Proveedor C", "region": "Este", "capacidad": 950},
    "prov4": {"nombre": "Proveedor D", "region": "Oeste", "capacidad": 1200},
    "prov5": {"nombre": "Proveedor E", "region": "Centro", "capacidad": 1100},
    "prov6": {"nombre": "Proveedor F", "region": "Norte", "capacidad": 700},
    "prov7": {"nombre": "Proveedor G", "region": "Sur", "capacidad": 900},
    "prov8": {"nombre": "Proveedor H", "region": "Este", "capacidad": 600},
    "prov9": {"nombre": "Proveedor I", "region": "Oeste", "capacidad": 1300},
    "prov10": {"nombre": "Proveedor J", "region": "Centro", "capacidad": 1400}
}

stock_db = {
    1: {"producto_id": 1, "stock": 20},
    2: {"producto_id": 2, "stock": 5},
    3: {"producto_id": 3, "stock": 2},
    4: {"producto_id": 4, "stock": 12}
}

class StockUpdate(BaseModel):
    cantidad: int

class ReservaStock(BaseModel):
    producto_id: int
    cantidad: int

@router.put("/inventario/actualizar/{producto_id}")
def actualizar_stock(producto_id: int, data: StockUpdate):
    """
    Actualiza la cantidad de stock para un producto.
    Parámetros:
        producto_id: identificador del producto.
        data: objeto con la cantidad actualizada.
    Comportamiento:
        simula la conexión al almacén físico, actualiza el stock en el repositorio en memoria y retorna el estado.
    """
    # [Desperdicio - Tiempos de espera]: simulando conexión al almacén físico
    time.sleep(2)
    stock_db.setdefault(producto_id, {"producto_id": producto_id, "stock": 0})
    stock_db[producto_id]["stock"] = data.cantidad
    return {"message": "Stock actualizado", "producto_id": producto_id, "stock": stock_db[producto_id]["stock"]}

@router.post("/inventario/reservar")
def reservar_stock(reserva: ReservaStock):
    """
    Reserva stock para una orden.
    Parámetros:
        reserva: objeto con producto_id y cantidad a reservar.
    Comportamiento:
        deduce la cantidad reservada del stock disponible y retorna el nuevo stock junto con un mensaje de alerta.
    """
    stock = stock_db.get(reserva.producto_id, {"stock": 0})["stock"]
    # [Bug - Condición de Carrera]: No valida si el stock final será negativo
    stock_db[reserva.producto_id] = {"producto_id": reserva.producto_id, "stock": stock - reserva.cantidad}
    nuevo_stock = stock_db[reserva.producto_id]["stock"]
    alerta = "" if nuevo_stock != 10 else "Stock bajo: solo quedan 10 unidades"
    return {"producto_id": reserva.producto_id, "stock": nuevo_stock, "alerta": alerta}

@router.get("/inventario/prediccion_demanda_ia")
def prediccion_demanda_ia():
    """
    Genera una predicción de demanda mock.
    Comportamiento:
        devuelve datos de pronóstico aleatorios que simulan una herramienta de inteligencia de demanda.
    """
    # [Desperdicio - Sobreingeniería]: endpoint falso con datos aleatorios
    return {
        "predictivo": [random.randint(1, 100) for _ in range(5)],
        "mensaje": "Predicción de demanda generada (mock)"
    }
