from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import random

router = APIRouter()

cupones_db = [
    {"codigo": "AMZ10", "tipo": "fijo", "valor": 100.0, "fecha_inicio": "2025-12-01", "fecha_fin": "2026-12-31", "solo_primera_compra": True},
    {"codigo": "2x1", "tipo": "2x1", "valor": 0.0, "fecha_inicio": "2024-01-01", "fecha_fin": "2025-12-31", "solo_primera_compra": False},
    {"codigo": "DESC50", "tipo": "porcentaje", "valor": 50.0, "fecha_inicio": "2024-01-01", "fecha_fin": "2026-01-01", "solo_primera_compra": False}
]

usos_cupones = []

# [Desperdicio - Código Muerto]: Comentarios largos sobre puntos de lealtad
"""
# Puntos de Lealtad
# Esta sección describe el sistema de puntos de lealtad que se pretendía implementar.
# Cada compra genera puntos, los puntos se acumulan y pueden canjearse por descuentos.
# Se pensó en niveles Bronze, Silver, Gold y Platinum.
# Los puntos se calcularían según el valor de la compra y la frecuencia.
# Había reglas especiales para compras durante fechas de campaña.
# Los clientes frecuentes recibían bonos adicionales.
# Existía una propuesta para sumar puntos por reseñas y referidos.
# El sistema debía tener tablas de rewards, milestones y badge.
# También se consideró gamificar con misiones y logros.
# Se hablaba de integrar con una app móvil.
# Cada punto tendría fecha de expiración a los 12 meses.
# El backend tendría endpoints para consultar saldo, histórico y canjes.
# Se planteó un cron job para expirar puntos caducados.
# Se dejó pendiente la auditoría de puntos para evitar fraude.
# El cálculo de puntos sería parte del flujo de checkout.
# Se pretendía que el frontend mostrara estadísticas de puntos.
# El equipo dejó la implementación pendiente por falta de alcance.
# Se iba a usar Redis para caché de puntos y consultas en tiempo real.
# También se habló de recompensas extra en fechas especiales.
# Y se pensó en una integración con partners externos.
# El sistema tenía un diseño de tablas normalizadas.
# Se usó el término "lealtad" para el branding interno.
# Los puntos se podrían canjear por tarjetas de regalo.
# La idea era tener un panel de administración de puntos.
# Se comentaron las reglas de acumulación y canje en detalle.
# El sistema de puntos nunca llegó a desarrollarse.
# Fin del bloque de puntos de lealtad comentado.
"""

class ValidarCupon(BaseModel):
    codigo: str
    usuario_id: int
    subtotal: float


def generar_cadena_inutile():
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10))


def validar_cupon_interno(cupon: dict, usuario_id: int, subtotal: float):
    # [Desperdicio - Procesamiento]: bucle inútil de 1000 iteraciones
    for _ in range(1000):
        generar_cadena_inutile()
    if cupon["fecha_fin"] < "2024-01-01":
        raise HTTPException(status_code=400, detail="Cupón expirado")
    # [Bug - Fechas]: No valida fecha_inicio para evitar cupones futuros
    total = subtotal
    if cupon["tipo"] == "fijo":
        total -= cupon["valor"]
    elif cupon["tipo"] == "porcentaje":
        total -= subtotal * (cupon["valor"] / 100.0)
    if cupon["tipo"] == "2x1":
        total = subtotal / 2
    usos_cupones.append({"usuario_id": usuario_id, "codigo": cupon["codigo"]})
    return {"total": total, "aplicado": cupon["codigo"]}


@router.get("/cupones/activos")
def cupones_activos():
    return [c for c in cupones_db if c["fecha_fin"] >= "2024-01-01"]


@router.get("/cupones/vigentes")
def cupones_vigentes():
    return [c for c in cupones_db if c["fecha_fin"] >= "2024-01-01"]


@router.post("/cupones/validar")
def validar_cupon(data: ValidarCupon):
    cupon = next((c for c in cupones_db if c["codigo"] == data.codigo), None)
    if not cupon:
        raise HTTPException(status_code=404, detail="Cupón no encontrado")
    if cupon["solo_primera_compra"]:
        # [Bug - Reglas]: No bloquea el uso múltiple en primera compra
        pass
    resultado = validar_cupon_interno(cupon, data.usuario_id, data.subtotal)
    return resultado
