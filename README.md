# Banano SaaS Backend

API para registrar, revisar y aprobar reportes de control de calidad en procesos bananeros. El backend esta construido con FastAPI, SQLAlchemy, Alembic y MySQL. La API alimentara una app movil hecha con React Native/Expo.

## Stack

- Python 3.11
- FastAPI
- SQLAlchemy 2
- Alembic
- MySQL 8
- Docker / Docker Compose
- Pytest

## Estructura del proyecto

```text
backend/
  alembic/
    versions/              # Migraciones de base de datos
    env.py
  app/
    api/v1/endpoints/      # Rutas HTTP
    core/                  # Configuracion, seguridad, permisos, errores
    crud/                  # Operaciones directas contra DB
    db/                    # Engine, session y metadata
    dependencies/          # Dependencias FastAPI, auth actual
    docs/                  # Documentacion funcional para frontend/API
    models/                # Modelos SQLAlchemy
    schemas/               # Schemas Pydantic
    services/              # Reglas de negocio
    main.py                # App FastAPI
  tests/                   # Suite pytest
  Dockerfile
  requirements.txt
```

La separacion sigue una idea de arquitectura limpia:

- `endpoints`: reciben requests, resuelven dependencias y traducen errores HTTP.
- `services`: contienen reglas de negocio, permisos, transiciones de estado y validaciones.
- `crud`: contiene acceso a datos sin reglas complejas.
- `models`: definen tablas y relaciones SQLAlchemy.
- `schemas`: definen contratos de entrada/salida de la API.
- `core`: centraliza seguridad, permisos y errores.

## Como levantar el proyecto

Desde la raiz del proyecto, donde esta `docker-compose.yml`:

```bash
docker compose up --build
```

En segundo plano:

```bash
docker compose up --build -d
```

La API queda disponible en:

```text
http://localhost:8000
```

Documentacion interactiva:

```text
http://localhost:8000/docs
```

Health check:

```text
GET /health
```

DB check:

```text
GET /db-check
```

## Migraciones

Alembic se ejecuta automaticamente al levantar el contenedor `api`:

```bash
alembic -c alembic.ini upgrade head
```

La revision actual esperada es:

```text
4c0f8d2a6e91
```

Para verificar:

```bash
docker compose exec api alembic -c alembic.ini current
```

## Autenticacion

La API usa JWT Bearer tokens.

Login:

```text
POST /auth/login
```

Body `application/x-www-form-urlencoded`:

```text
username=admin@test.com
password=123456
```

Response:

```json
{
  "access_token": "...",
  "access_expires_at": "...",
  "refresh_token": "...",
  "refresh_expires_at": "..."
}
```

Todos los endpoints protegidos usan:

```text
Authorization: Bearer <access_token>
```

Refresh:

```text
POST /auth/refresh
```

Logout:

```text
POST /auth/logout
```

## Usuarios de prueba

El seed deja usuarios listos para probar la app movil:

```text
admin@test.com       / 123456
evaluador@test.com   / 123456
supervisor@test.com  / 123456
```

Roles:

- `evaluador`
- `supervisor`
- `admin`

## Permisos por rol

### Evaluador

- Puede leer catalogos, productores, haciendas y lotes de su empresa.
- Puede crear reportes en `draft`.
- Puede ver, editar y enviar solo sus propios reportes.
- No puede iniciar revision, aprobar, rechazar ni reabrir.

### Supervisor

- Puede leer datos de su empresa.
- Puede ver reportes de su empresa.
- Puede iniciar revision de reportes `submitted`.
- Puede aprobar o rechazar reportes `under_review`.
- No puede crear, editar, enviar ni reabrir reportes.

### Admin

- Puede operar reportes de su empresa.
- Puede crear, editar, enviar, iniciar revision, aprobar y rechazar.
- Puede reabrir reportes `approved` con comentario obligatorio.

Ningun usuario puede ver datos de otra empresa.

## Concepto principal: Reporte como cabecera

La tabla `reportes` funciona como cabecera comun. Desde ella se derivan los detalles especificos segun el tipo:

```text
Reporte
  tipo = reporte_de_gancho
    -> ReporteGanchoDetalle
    -> ReporteGanchoCinta
    -> ReporteGanchoMotivo

Reporte
  tipo = terminados_de_proceso
    -> TerminadoProcesoDetalle
    -> TerminadoLote
    -> TerminadoLoteMarca
```

Esto permite que ambos tipos compartan:

- empresa
- productor
- hacienda
- semana
- fecha
- creador/evaluador
- estado del workflow
- historial de revision
- permisos
- listado, filtros y paginacion

## Tipos de reporte

### `reporte_de_gancho`

Registra informacion de racimos, cintas y motivos de rechazo.

Partes principales:

- detalle de gancho
- cintas por color
- motivos por catalogo

Catalogos usados:

- `GET /catalogos/colores`
- `GET /catalogos/motivos`

### `terminados_de_proceso`

Registra informacion de terminado segun el formato operativo usado por los trabajadores.

Partes principales:

- detalle general: exportadora, camion, vapor, puerto, codigo, sello, placa, chofer, calificador, hora de termino
- lotes
- marcas por lote
- cajas por marca

Catalogos usados:

- `GET /catalogos/marcas`
- `GET /haciendas/{id}/lotes`

El campo `total_cajas` se calcula en backend sumando las cajas de las marcas por lote.

El evaluador oficial sale de `reporte.created_by_user_id`. El terminado guarda tambien un snapshot operativo:

- `evaluador_nombre_texto`
- `evaluador_ci`

Estos se autocompletan desde el usuario autenticado si el cliente no los envia.

## Flujo de estados

Estados:

```text
draft
submitted
under_review
needs_changes
approved
```

Transiciones:

```text
draft -> submitted
needs_changes -> submitted
submitted -> under_review
under_review -> approved
under_review -> needs_changes
approved -> needs_changes
```

Detalle:

- `draft`: editable por evaluador creador o admin.
- `submitted`: enviado, no editable.
- `under_review`: tomado por supervisor/admin.
- `needs_changes`: vuelve a ser editable.
- `approved`: cerrado. Solo admin puede reabrir.

`GET /reportes/{id}` devuelve `allowed_actions`, que indica que acciones puede hacer el usuario autenticado.

Ejemplo:

```json
{
  "allowed_actions": ["edit_header", "save_detail", "submit"]
}
```

Posibles acciones:

```text
edit_header
save_detail
submit
start_review
approve
reject
reopen
```

## Endpoints principales

### Catalogos y datos para formularios

```text
GET /productores
GET /haciendas?productor_id={id}
GET /haciendas/{hacienda_id}/lotes
GET /catalogos/colores
GET /catalogos/motivos
GET /catalogos/marcas
```

Todos filtran por `actor_user.empresa_id`.

### Reportes

Crear draft:

```text
POST /reportes/drafts
```

Editar cabecera:

```text
PATCH /reportes/{id}/draft
```

Guardar gancho:

```text
PUT /reportes/{id}/gancho
```

Guardar terminado:

```text
PUT /reportes/{id}/terminado
```

Enviar:

```text
POST /reportes/{id}/submit
```

Iniciar revision:

```text
POST /reportes/{id}/start-review
```

Revisar:

```text
POST /reportes/{id}/review
```

Body:

```json
{
  "accion": "aprobado",
  "comentario": "Todo correcto"
}
```

Reabrir:

```text
POST /reportes/{id}/reopen
```

Body:

```json
{
  "comentario": "Se reabre para corregir datos"
}
```

Detalle:

```text
GET /reportes/{id}
```

Listado con filtros:

```text
GET /reportes
```

Filtros soportados:

```text
estado
tipo
semana_reporte
productor_id
hacienda_id
fecha_desde
fecha_hasta
search
order_by
order_dir
limit
offset
```

`order_by` permitido:

```text
id
fecha_reporte
semana_reporte
```

## Responses importantes

### Reporte basico

```json
{
  "id": 1,
  "empresa_id": 1,
  "hacienda_id": 1,
  "productor_id": 1,
  "created_by_user_id": 1,
  "tipo": "reporte_de_gancho",
  "estado": "draft",
  "supervisor_id": null,
  "submitted_at": null,
  "semana_reporte": 35,
  "fecha_reporte": "2025-08-28"
}
```

### Detalle de reporte

Incluye:

- header del reporte
- empresa
- productor
- hacienda
- usuario creador
- supervisor
- detalle de gancho si aplica
- detalle de terminado si aplica
- historial
- `allowed_actions`

### Listado

```json
{
  "total": 10,
  "limit": 20,
  "offset": 0,
  "items": []
}
```

## Errores HTTP

La API usa:

- `400`: datos invalidos o regla de negocio de validacion.
- `401`: no autenticado.
- `403`: usuario autenticado sin permiso para la accion.
- `404`: recurso inexistente o no accesible para el usuario.

## Tests

La suite usa Pytest, FastAPI TestClient y SQLite temporal.

Ejecutar dentro del contenedor:

```bash
docker compose exec api python -m pytest -q
```

Cobertura actual:

- crear draft
- guardar gancho
- submit
- start-review
- review aprobado/rechazado
- terminado
- filtros, busqueda y paginacion
- catalogos

Resultado esperado:

```text
8 passed
```

## Documentacion adicional

Dentro de `app/docs`:

```text
frontend_endpoints.md
mobile_screens.md
permissions.md
report_status_flow.md
```

Estos archivos resumen:

- endpoints para frontend
- pantallas moviles sugeridas
- permisos por rol
- flujo de estados

## Notas de base de datos

Se corrigio una inconsistencia historica:

- `haciendas.id` ahora es `AUTO_INCREMENT` en MySQL.
- El modelo ya lo declaraba asi, pero la DB real no lo tenia aplicado.

Migracion relacionada:

```text
4c0f8d2a6e91_fix_haciendas_id_autoincrement.py
```

## Estado actual del backend

El backend ya cubre:

- datos para formularios moviles
- reportes tipo gancho
- reportes tipo terminado de proceso
- workflow completo de revision
- reapertura admin
- permisos por rol
- aislamiento por empresa
- catalogos por empresa
- tests automatizados
- seed para pruebas frontend

Pendientes posibles para futuras fases:

- normalizar schemas viejos no usados.
- eliminar o migrar legado `terminado_marcas`.
- ampliar tests de seguridad y errores.
- mejorar seed para multiples empresas completas.
- agregar endpoints admin para gestionar catalogos desde la app.
