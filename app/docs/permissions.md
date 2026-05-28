# Permisos por rol

## Evaluador

- Puede leer catalogos, productores, haciendas y lotes de su empresa.
- Puede crear reportes en estado `draft`.
- Puede ver, editar detalles y enviar solo reportes creados por el mismo.
- No puede iniciar revision, aprobar, rechazar ni reabrir reportes.

## Supervisor

- Puede leer catalogos, productores, haciendas y lotes de su empresa.
- Puede ver reportes de su empresa.
- Puede iniciar revision de reportes `submitted`.
- Puede aprobar o rechazar reportes `under_review`.
- No puede crear, editar, enviar ni reabrir reportes.

## Admin

- Puede leer catalogos, productores, haciendas y lotes de su empresa.
- Puede crear, editar y enviar reportes de su empresa.
- Puede iniciar revision, aprobar y rechazar reportes de su empresa.
- Puede reabrir reportes `approved` con comentario obligatorio.

## Aislamiento por empresa

- Ningun usuario puede leer ni modificar reportes de otra empresa.
- Los catalogos se filtran siempre por `actor_user.empresa_id`.
- Los productores, haciendas y lotes se filtran siempre por `actor_user.empresa_id`.
- En listados de reportes, evaluador solo recibe sus propios reportes; supervisor/admin reciben los reportes de su empresa.
