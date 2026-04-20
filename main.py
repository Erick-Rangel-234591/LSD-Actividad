from fastapi import FastAPI
from routers import usuarios, catalogo, inventario, carrito, pedidos, promociones, pagos, envios, resenas

app = FastAPI(title="Proyecto LSD: Amazonas API", version="1.0.0")

app.include_router(usuarios.router, prefix="/usuarios", tags=["Equipo 1 - Usuarios"])
app.include_router(catalogo.router, prefix="/catalogo", tags=["Equipo 2 - Catálogo"])
app.include_router(inventario.router, prefix="/inventario", tags=["Equipo 3 - Inventario"])
app.include_router(carrito.router, prefix="/carrito", tags=["Equipo 4 - Carrito"])
app.include_router(pedidos.router, prefix="/pedidos", tags=["Equipo 5 - Pedidos"])
app.include_router(promociones.router, prefix="/promociones", tags=["Equipo 6 - Promociones"])
app.include_router(pagos.router, prefix="/pagos", tags=["Equipo 8 - Pagos"])
app.include_router(envios.router, prefix="/envios", tags=["Equipo 9 - Envíos"])
app.include_router(resenas.router, prefix="/resenas", tags=["Equipo 10 - Reseñas"])

@app.get("/")
def root():
    return {"message": "Amazonas API corriendo!"}
