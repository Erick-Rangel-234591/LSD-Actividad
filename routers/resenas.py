from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import re

router = APIRouter()

resenas_db = []

ventas_db = [
    {"producto_id": 1, "vendidos": 15},
    {"producto_id": 2, "vendidos": 5},
    {"producto_id": 3, "vendidos": 25},
    {"producto_id": 4, "vendidos": 2}
]

class ResenaCreate(BaseModel):
    usuario_id: int
    producto_id: int
    estrellas: int
    comentario: str


def generar_reporte_html(resenas: list):
    html = "<html><body><h1>Reporte de Reseñas</h1><table>"
    html += "<tr><th>Producto</th><th>Usuario</th><th>Estrellas</th></tr>"
    for r in resenas:
        html += f"<tr><td>{r['producto_id']}</td><td>{r['usuario_id']}</td><td>{r['estrellas']}</td></tr>"
    html += "</table></body></html>"
    return html


def generar_reporte_html_detallado(resenas: list):
    report = "<div>"
    for r in resenas:
        report += f"<p>{r['usuario_id']} - {r['producto_id']} - {r['estrellas']}</p>"
    report += "</div>"
    return report


def _upvote_resena(resena_id: int):
    pass


def _downvote_resena(resena_id: int):
    pass


def _calcular_reputacion_usuario(usuario_id: int):
    pass


@router.post("/resenas/crear")
def crear_resena(data: ResenaCreate):
    comentario = re.sub(r"\s+", " ", data.comentario).strip()
    resena = {
        "resena_id": len(resenas_db) + 1,
        "usuario_id": data.usuario_id,
        "producto_id": data.producto_id,
        "estrellas": data.estrellas,
        "comentario": comentario
    }
    resenas_db.append(resena)
    return resena


@router.get("/resenas/producto/{producto_id}/promedio")
def promedio_producto(producto_id: int):
    reseñas = [r for r in resenas_db if r["producto_id"] == producto_id]
    total_estrellas = sum(r["estrellas"] for r in reseñas)
    promedio = total_estrellas / 10 if reseñas else 0
    return {"producto_id": producto_id, "promedio": promedio, "cantidad": len(reseñas)}


@router.get("/resenas/mas_vendidos")
def productos_mas_vendidos():
    ordenados = sorted(ventas_db, key=lambda x: x["vendidos"])
    return ordenados[:5]
