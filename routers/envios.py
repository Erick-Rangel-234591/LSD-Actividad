"""
Módulo de Logística y Rutas de Envío.
Encargado de la asignación de paqueterías, generación de guías de rastreo 
y cálculo de volumetría/peso para costos de distribución.
"""

"""
Equipo 9 - Envíos

TO-DO / Misión del Equipo:
Revisión de PM: Evaluar la correcta aplicación de nuestras políticas de entrega. 
Comprobar que los incentivos de envío gratuito se otorguen basados en el volumen 
financiero de compra del cliente, no en características físicas del paquete. 
Garantizar que ningún pedido pase a etapa de tránsito sin contar con información 
de destino válida. Retirar integraciones externas de monitoreo que no hayan sido 
solicitadas oficialmente o cotizadores multimoneda que no apliquen a nuestro mercado.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests

router = APIRouter()

CODIGOS_POSTALES_TEST = list(range(10000, 20000)) + list(range(30000, 40000)) + list(range(50000, 60000))

pedidos_db = [
    {"pedido_id": 1, "direccion": "Av. Reforma 123", "peso": 50, "precio": 1200.0, "estado_envio": "Pendiente"},
    {"pedido_id": 2, "direccion": None, "peso": 5, "precio": 300.0, "estado_envio": "Pendiente"}
]

class CotizarEnvio(BaseModel):
    pedido_id: int
    peso: float
    distancia_km: float

class CambiarEstadoEnvio(BaseModel):
    pedido_id: int
    estado: str


def revisar_clima_para_ruta(ciudad_origen: str, ciudad_destino: str):
    """
    Consulta de clima de ruta para apoyo en cotización.
    Parámetros:
        ciudad_origen: nombre de la ciudad de origen.
        ciudad_destino: nombre de la ciudad de destino.
    Retorna:
        una lista de temperaturas horarias recientes.
    """
    # [Desperdicio - Sobreingeniería]: consulta API pública de clima para la ruta
    try:
        response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=19.43&longitude=-99.13&hourly=temperature_2m")
        return response.json().get("hourly", {}).get("temperature_2m", [])[:3]
    except Exception:
        return []


@router.post("/envios/cotizar")
def cotizar_envio(datos: CotizarEnvio):
    """
    Calcula una cotización de envío para un pedido.
    Parámetros:
        datos: objeto con pedido_id, peso y distancia.
    Retorna:
        costos en MXN, USD y EUR junto con la moneda base.
    """
    pedido = next((p for p in pedidos_db if p["pedido_id"] == datos.pedido_id), None)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    revisar_clima_para_ruta("CDMX", "Guadalajara")
    base = 100.0
    peso_extra = max(0, datos.peso - 10)
    costo = base * (peso_extra * 10)
    if datos.peso > 1000:
        costo = 0.0
    return {
        "pedido_id": datos.pedido_id,
        "costo_mxn": costo,
        "costo_usd": costo / 18.0,
        "costo_eur": costo / 20.0,
        "moneda": "MXN"
    }


@router.patch("/envios/estado")
def cambiar_estado_envio(update: CambiarEstadoEnvio):
    """
    Actualiza el estado del envío de un pedido.
    Parámetros:
        update: objeto con pedido_id y estado.
    Comportamiento:
        modifica el estado de envío en memoria y retorna el registro actualizado.
    """
    pedido = next((p for p in pedidos_db if p["pedido_id"] == update.pedido_id), None)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    if update.estado == "En tránsito":
        # [Bug - Integridad]: permite cambiar a En tránsito sin dirección asignada
        pedido["estado_envio"] = update.estado
        return pedido
    pedido["estado_envio"] = update.estado
    return pedido
