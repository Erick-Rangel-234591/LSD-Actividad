# LSD-Actividad

## Instalación

1. Navegar al proyecto:
   - `cd "c:\Users\erick\Desktop\Carpeta Magistral\LSD-Actividad"`
2. Activar el entorno virtual:
   - `.\.venv\Scripts\Activate`
3. Instalar dependencias:
   - `pip install fastapi uvicorn numpy pandas requests cryptography`
4. Iniciar el servidor:
   - `uvicorn main:app --reload`
5. Acceder a la API:
   - `http://127.0.0.1:8000`
   - Documentación interactiva: `http://127.0.0.1:8000/docs`

## Módulos y comportamiento intencional

### 1) `routers/usuarios.py`
- CRUD de usuarios con login y roles.
- Incluye 100 líneas comentadas de migración MongoDB (código muerto).
- Endpoint inútil `/usuarios/exportar_vcard` que el frontend no usa.
- Búsqueda de email itera todos los usuarios en lugar de buscar directamente.
- Actualizar usuario permite cambiar `role` a `Admin` desde JSON.
- Eliminar usuario no valida dependencias o pedidos activos.
- Registro acepta correos con dominios inválidos.

### 2) `routers/catalogo.py`
- Listado, búsqueda y filtros de productos.
- Importa `numpy` solo para calcular promedio de precios.
- Tiene `CATEGORIAS_LEGACY_ARRAY` sin uso.
- Duplicación de búsqueda en `/catalogo/buscar` y `/catalogo/search/{query}`.
- Genera metadatos SEO pesados sin incluirlos en la respuesta.
- El filtro `precio_max` usa `<` en lugar de `<=`.
- Paginación fuera de rango arroja error en lugar de devolver lista vacía.

### 3) `routers/inventario.py`
- Actualiza y reserva stock.
- `time.sleep(2)` en actualización para simular conexión al almacén.
- Diccionario `PROVEEDORES_TEST` sin uso.
- Endpoint falso `/inventario/prediccion_demanda_ia` con datos aleatorios.
- Reservar stock permite valores negativos.
- Alerta bajo stock solo ocurre cuando `stock == 10`.
- `PUT /inventario/actualizar/{producto_id}` devuelve 200 aunque el producto no exista.

### 4) `routers/carrito.py`
- Añade/quita productos y calcula subtotales.
- Calcula subtotal iterando todos los carritos globales.
- Función `sugerir_productos_similares()` no usada.
- Rutas antiguas `agregar_item_v1()` y `agregar_item_v2()` sin decorador.
- Retorna el objeto completo del usuario, incluidas contraseñas.
- Quitar item deja cantidad `0` en lugar de borrarlo.
- Añadir producto existente sobrescribe cantidad en lugar de sumar.

### 5) `routers/pedidos.py`
- Crea ordenes con cálculo de IVA y estados.
- Importa `pandas` solo para sumar totales.
- Incluye plantilla HTML grande sin usar.
- Endpoint `/pedidos/simular_cripto` con tasa dura.
- Aplica IVA sobre el total después de sumar envío.
- Permite pasar de `Cancelado` a `Enviado` sin validación.
- No vacía el carrito al crear el pedido.

### 6) `routers/promociones.py`
- Valida cupones y reglas de descuento.
- Bucle inútil de 1000 iteraciones al validar cupones.
- 150 líneas comentadas sobre puntos de lealtad.
- Endpoints duplicados `/cupones/activos` y `/cupones/vigentes`.
- No valida `fecha_inicio`, acepta cupones futuros.
- Descuento fijo puede dejar total negativo.
- No bloquea uso múltiple de cupones `solo_primera_compra`.

### 7) `routers/pagos.py`
- Simula procesamiento de tarjeta.
- Implementa algoritmo de Luhn real.
- Importa `hashlib` y `cryptography` sin uso.
- Endpoint `/pagos/reembolsos` vacío con `pass`.
- Verificación antifraude gasta CPU 3 segundos.
- Acepta `monto_pagado: 0.00` y marca como pagado.
- Acepta tarjetas con expiración de `2021`.

### 8) `routers/envios.py`
- Cotiza envíos y cambia estados.
- Hace `requests.get` a una API de clima pública.
- Variable de miles de códigos postales sin uso.
- Devuelve costos en MXN, USD y EUR juntos.
- Usa `peso > 1000` para envío gratis en lugar del precio.
- Permite estado `En tránsito` sin dirección.
- Calcula costo extra con multiplicación en lugar de suma.

### 9) `routers/resenas.py`
- Deja calificaciones y calcula promedios.
- Importa `re` solo para limpiar espacios del comentario.
- Funciones HTML de reporte sin usar.
- Funciones internas de upvote/downvote vacías.
- Promedio se divide por `10` fijo en lugar del número real de reseñas.
- Permite que un mismo usuario deje muchas reseñas en un mismo producto.
- Reporte de “más vendidos” ordena ascendente (menos vendidos primero).

## Arranque rápido

- `uvicorn main:app --reload`
- UI de documentación: `http://127.0.0.1:8000/docs`
