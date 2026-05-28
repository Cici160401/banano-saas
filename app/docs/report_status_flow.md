# Flujo de estados de reportes

## Estados

- `draft`: borrador editable por evaluador creador o admin.
- `submitted`: enviado para revision; ya no es editable.
- `under_review`: tomado por supervisor/admin para revision.
- `needs_changes`: rechazado o reabierto; vuelve a ser editable.
- `approved`: aprobado y cerrado; solo admin puede reabrirlo.

## Transiciones

- `draft -> submitted`: evaluador creador o admin envia el reporte.
- `needs_changes -> submitted`: evaluador creador o admin reenvia correcciones.
- `submitted -> under_review`: supervisor/admin inicia revision.
- `under_review -> approved`: supervisor/admin aprueba.
- `under_review -> needs_changes`: supervisor/admin rechaza con comentario opcional.
- `approved -> needs_changes`: admin reabre con comentario obligatorio.

## Acciones por estado

- `draft`: `edit_header`, `save_detail`, `submit`.
- `submitted`: `start_review` para supervisor/admin.
- `under_review`: `approve`, `reject` para supervisor/admin.
- `needs_changes`: `edit_header`, `save_detail`, `submit`.
- `approved`: `reopen` para admin.

`GET /reportes/{id}` devuelve `allowed_actions` calculado para el usuario autenticado.
