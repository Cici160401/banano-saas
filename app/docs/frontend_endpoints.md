# Endpoints para frontend movil

Base local: `http://localhost:8000`

## Auth

`POST /auth/login`

Body form-data:

- `username`: email
- `password`: password

Response:

- `access_token`
- `refresh_token`
- `access_expires_at`
- `refresh_expires_at`

Usar `Authorization: Bearer <access_token>` en endpoints protegidos.

## Datos para formularios

`GET /productores`

Response item:

- `id`
- `codigo_productor`
- `nombre`

`GET /haciendas?productor_id={id}`

Response item:

- `id`
- `codigo_hacienda`
- `nombre`
- `zona`

`GET /haciendas/{hacienda_id}/lotes`

Response item:

- `id`
- `numero_lote`

`GET /catalogos/colores`

Response item:

- `id`
- `nombre`
- `hex`

`GET /catalogos/motivos`

Response item:

- `id`
- `nombre`

`GET /catalogos/marcas`

Response item:

- `id`
- `nombre`

## Reportes

`POST /reportes/drafts`

Body:

- `empresa_id`: ignorado por backend; se toma del usuario autenticado
- `tipo`: `reporte_de_gancho` o `terminados_de_proceso`
- `productor_id`: opcional en draft
- `hacienda_id`: opcional en draft
- `semana_reporte`: opcional en draft
- `fecha_reporte`: opcional en draft

`PATCH /reportes/{id}/draft`

Actualiza header editable: `productor_id`, `hacienda_id`, `semana_reporte`, `fecha_reporte`.

`PUT /reportes/{id}/gancho`

Guarda detalle, cintas y motivos del reporte de gancho.

`PUT /reportes/{id}/terminado`

Guarda detalle de terminado, lotes y marcas por lote.

`POST /reportes/{id}/submit`

Envia el reporte a revision.

`POST /reportes/{id}/start-review`

Supervisor/admin toma el reporte para revision.

`POST /reportes/{id}/review`

Body:

- `accion`: `aprobado` o `rechazado`
- `comentario`: opcional

`POST /reportes/{id}/reopen`

Solo admin. Body:

- `comentario`: obligatorio

`GET /reportes/{id}`

Devuelve header, relaciones, detalle de gancho o terminado, historial y `allowed_actions`.

`GET /reportes`

Filtros:

- `estado`
- `tipo`
- `semana_reporte`
- `productor_id`
- `hacienda_id`
- `fecha_desde`
- `fecha_hasta`
- `search`
- `order_by`: `id`, `fecha_reporte`, `semana_reporte`
- `order_dir`: `asc`, `desc`
- `limit`
- `offset`
