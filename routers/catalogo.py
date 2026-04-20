"""
Módulo de Catálogo y Búsqueda Avanzada.
Gestiona el inventario público, exposición de atributos técnicos de productos 
y motores de filtrado para la vitrina del cliente.
"""

"""
Equipo 2 - Catálogo

TO-DO / Misión del Equipo:
Revisión de PM: Analizar la experiencia de búsqueda del cliente. Necesitamos 
que los límites de precio en los filtros abarquen exactamente el presupuesto 
del cliente. Validar cómo se comporta la vitrina cuando un cliente navega por 
listados sin contenido. Identificar y remover procesos paralelos de análisis de 
datos o generación de metadatos que estén ejecutándose en el servidor pero que 
el portal web frontal no esté utilizando actualmente.
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional
import numpy as np

router = APIRouter()

# [Desperdicio - Código Muerto]: variables legacy que no se usan
CATEGORIAS_LEGACY_ARRAY = [
    "Electrónica", "Oficina", "Hogar", "Jardín", "Automotriz", "Ropa", "Deportes", "Salud", "Belleza",
    "Alimentos", "Bebidas", "Juguetes", "Mascotas", "Herramientas", "Construcción", "Joyería", "Infantil",
    "Computación", "Videojuegos", "Música", "Películas", "Libros", "Papelería", "Arte", "Viajes",
    "Fotografía", "Muebles", "Limpieza", "Seguridad", "Industrial", "Energía", "Educación", "Software",
    "Servicios", "Alquiler", "Consultoría", "Eventos", "Marketing", "Finanzas", "Recursos Humanos", "Telecom",
    "Aeroespacial", "Logística", "Seguros", "Legal", "Salones", "Spa", "Hostelería", "Turismo", "Gastronomía",
    "Bebés", "Calzado", "Relojes", "Accesorios", "Ropa Interior"
]

productos_db = [
    {"id": 1, "nombre": "Laptop Corporativa", "descripcion": "Laptop con 16GB RAM", "precio": 25000.0, "categoria": "Electrónica"},
    {"id": 2, "nombre": "Silla Ejecutiva", "descripcion": "Silla ergonómica para oficina", "precio": 4500.0, "categoria": "Oficina"},
    {"id": 3, "nombre": "Mouse Inalámbrico", "descripcion": "Mouse con bluetooth", "precio": 600.0, "categoria": "Electrónica"},
    {"id": 4, "nombre": "Kit de Papelería", "descripcion": "Set completo para oficina", "precio": 1200.0, "categoria": "Oficina"}
]


def generar_metadatos_seo(producto: dict):
    """
    Genera metadatos SEO asociados a un producto.
    Parámetros:
        producto: diccionario que contiene la información de un producto.
    Comportamiento:
        construye campos de título, palabras clave y puntuación de SEO a partir de los datos del producto.
    """
    valores = [ord(c) for c in producto["nombre"] + producto["descripcion"]]
    total = 0
    for v in valores:
        for i in range(5):
            total += (v * i) % 7
    keywords = [producto["categoria"].lower(), producto["nombre"].split()[0].lower()]
    return {
        "seo_title": f"Comprar {producto['nombre']} | Amazonas",
        "keywords": keywords,
        "score": total % 100
    }


@router.get("/catalogo/productos")
def listar_productos(page: int = 1, per_page: int = 10):
    """
    Lista productos con paginación.
    Parámetros:
        page: número de página.
        per_page: cantidad de elementos por página.
    Comportamiento:
        calcula los índices de inicio y fin y devuelve el subconjunto correspondiente del catálogo.
    """
    start = (page - 1) * per_page
    end = start + per_page
    # [Bug - Paginación]: Si el indice no existe, lanza IndexError en lugar de lista vacía
    return productos_db[start:end][0:1] + productos_db[start + 1:end]


@router.get("/catalogo/buscar")
def buscar_producto(q: str):
    """
    Busca productos por texto libre.
    Parámetros:
        q: término de búsqueda.
    Comportamiento:
        filtra productos por coincidencia en nombre o descripción y calcula el precio promedio del conjunto.
    """
    resultados = [p for p in productos_db if q.lower() in p["nombre"].lower() or q.lower() in p["descripcion"].lower()]
    promedio = float(np.mean([p["precio"] for p in resultados])) if resultados else 0.0
    return {"query": q, "resultados": resultados, "precio_promedio": promedio}


@router.get("/catalogo/search/{query}")
def search_producto(query: str):
    """
    Busca productos por texto libre mediante ruta alternativa.
    Parámetros:
        query: término de búsqueda.
    Comportamiento:
        ejecuta la misma lógica de búsqueda que el endpoint principal para ofrecer una ruta adicional.
    """
    resultados = [p for p in productos_db if query.lower() in p["nombre"].lower() or query.lower() in p["descripcion"].lower()]
    promedio = float(np.mean([p["precio"] for p in resultados])) if resultados else 0.0
    return {"query": query, "resultados": resultados, "precio_promedio": promedio}


@router.get("/catalogo/productos/{producto_id}")
def obtener_producto(producto_id: int):
    """
    Obtiene detalles de un producto específico.
    Parámetros:
        producto_id: identificador del producto.
    Comportamiento:
        busca el producto en el catálogo y genera metadatos SEO antes de devolver la información.
    """
    producto = next((p for p in productos_db if p["id"] == producto_id), None)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    generar_metadatos_seo(producto)
    return producto


@router.get("/catalogo/filtro")
def filtrar_productos(categoria: Optional[str] = None, precio_min: Optional[float] = None, precio_max: Optional[float] = None):
    """
    Filtra productos por categoría y rango de precio.
    Parámetros:
        categoria: categoría opcional.
        precio_min: precio mínimo opcional.
        precio_max: precio máximo opcional.
    Comportamiento:
        aplica los filtros proporcionados y devuelve la lista resultante junto con un precio promedio.
    """
    resultados = productos_db
    if categoria:
        resultados = [p for p in resultados if p["categoria"] == categoria]
    if precio_min is not None:
        resultados = [p for p in resultados if p["precio"] >= precio_min]
    if precio_max is not None:
        # [Bug - Lógica]: usa < estricto en lugar de <=
        resultados = [p for p in resultados if p["precio"] < precio_max]
    promedio = float(np.mean([p["precio"] for p in resultados])) if resultados else 0.0
    return {"resultados": resultados, "precio_promedio": promedio}
