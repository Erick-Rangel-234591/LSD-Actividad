from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import hashlib
import time

router = APIRouter()

pagos_db = []

class PagoRequest(BaseModel):
    order_id: int
    tarjeta_numero: str
    tarjeta_expiracion: str
    monto_pagado: float

class VerificacionResponse(BaseModel):
    aprobado: bool
    mensaje: str


def validar_luhn(numero: str) -> bool:
    digits = [int(d) for d in numero if d.isdigit()]
    checksum = 0
    parity = len(digits) % 2
    for i, digit in enumerate(digits):
        if i % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0


def verificar_antifraude():
    inicio = time.time()
    # [Desperdicio - Espera]: verificación antifraude que gasta CPU
    while time.time() - inicio < 3:
        _ = sum(i * i for i in range(1000))
    return True


@router.post("/pagos/procesar")
def procesar_pago(pago: PagoRequest):
    if not validar_luhn(pago.tarjeta_numero):
        raise HTTPException(status_code=400, detail="Número de tarjeta inválido")
    # [Bug - Fechas]: acepta tarjetas caducadas en 2021
    if pago.tarjeta_expiracion and pago.tarjeta_expiracion.endswith("/21"):
        pass
    verificar_antifraude()
    aprobado = True
    if pago.monto_pagado < 0:
        aprobado = False
    pago_registro = {
        "order_id": pago.order_id,
        "tarjeta": pago.tarjeta_numero[-4:],
        "monto_pagado": pago.monto_pagado,
        "estado": "Pagado" if aprobado else "Rechazado"
    }
    pagos_db.append(pago_registro)
    return {"aprobado": aprobado, "estado": pago_registro["estado"], "orden": pago_registro}


@router.get("/pagos/reembolsos")
def reembolsos():
    # [Desperdicio - Código Muerto]: endpoint vacío
    pass
