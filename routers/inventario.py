from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import random
import time

router = APIRouter()

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
    # [Desperdicio - Tiempos de espera]: simulando conexión al almacén físico
    time.sleep(2)
    stock_db.setdefault(producto_id, {"producto_id": producto_id, "stock": 0})
    stock_db[producto_id]["stock"] = data.cantidad
    return {"message": "Stock actualizado", "producto_id": producto_id, "stock": stock_db[producto_id]["stock"]}

@router.post("/inventario/reservar")
def reservar_stock(reserva: ReservaStock):
    stock = stock_db.get(reserva.producto_id, {"stock": 0})["stock"]
    # [Bug - Condición de Carrera]: No valida si el stock final será negativo
    stock_db[reserva.producto_id] = {"producto_id": reserva.producto_id, "stock": stock - reserva.cantidad}
    nuevo_stock = stock_db[reserva.producto_id]["stock"]
    alerta = "" if nuevo_stock != 10 else "Stock bajo: solo quedan 10 unidades"
    return {"producto_id": reserva.producto_id, "stock": nuevo_stock, "alerta": alerta}

@router.get("/inventario/prediccion_demanda_ia")
def prediccion_demanda_ia():
    # [Desperdicio - Sobreingeniería]: endpoint falso con datos aleatorios
    return {
        "predictivo": [random.randint(1, 100) for _ in range(5)],
        "mensaje": "Predicción de demanda generada (mock)"
    }
