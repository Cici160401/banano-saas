# Pantallas moviles sugeridas

## Login

Endpoint principal:

- `POST /auth/login`

## Lista de reportes

Endpoints:

- `GET /reportes`
- `GET /reportes/{id}`

Controles:

- filtro por estado
- filtro por tipo
- busqueda por productor/hacienda
- paginacion con `limit` y `offset`

## Crear reporte

Endpoint:

- `POST /reportes/drafts`

Campos iniciales:

- tipo de reporte
- productor
- hacienda
- semana
- fecha

Datos auxiliares:

- `GET /productores`
- `GET /haciendas?productor_id={id}`

## Editar reporte de gancho

Endpoint:

- `PUT /reportes/{id}/gancho`

Datos auxiliares:

- `GET /catalogos/colores`
- `GET /catalogos/motivos`

Acciones:

- guardar borrador
- enviar si `allowed_actions` contiene `submit`

## Editar terminado de proceso

Endpoint:

- `PUT /reportes/{id}/terminado`

Datos auxiliares:

- `GET /catalogos/marcas`
- `GET /haciendas/{id}/lotes`

Acciones:

- guardar borrador
- enviar si `allowed_actions` contiene `submit`

## Revision supervisor/admin

Endpoints:

- `POST /reportes/{id}/start-review`
- `POST /reportes/{id}/review`

Acciones:

- iniciar revision si `allowed_actions` contiene `start_review`
- aprobar si contiene `approve`
- rechazar si contiene `reject`

## Reapertura admin

Endpoint:

- `POST /reportes/{id}/reopen`

Mostrar solo si `allowed_actions` contiene `reopen`.
