# app/services/reporte_service.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.hacienda import Hacienda
from app.models.empresa import Empresa
from app.models.productor import Productor
from app.models.reporte import Reporte
from app.models.enum import ReportStatus, ReportType
from app.models.reporte_revision import ReporteRevision
from app.schemas.reporte import ReporteReopen, ReporteReview
from app.schemas.reporte import ReporteUpdateDraft, ReporteCreateDraft
from app.crud import reporte as reporte_crud
from app.core.permissions import (
    can_create_or_edit_reporte,
    can_read_reporte,
    can_reopen_reporte,
    can_review_reporte,
)
from app.core.errors import BusinessRuleError
from datetime import timezone, datetime, date



##Eager Loading: Trae el objeto con TODOS sus atributos
##Lazy loading : Es el comportamiento por defecto ESTO TENGO AHORA PARA TRAER LOS DATOS CON SQL ALCHEMY


def make_revision(
    reporte: Reporte,
    actor_user: User,
    from_status: ReportStatus,
    to_status: ReportStatus,
    comentario: str | None = None,
) -> ReporteRevision:
    return ReporteRevision(
        reporte_id=reporte.id,
        actor_user_id=actor_user.id,
        from_status=from_status,
        to_status=to_status,
        comentario=comentario,
    )


def can_edit_report(actor_user: User, reporte: Reporte) -> bool:
    return (
        can_create_or_edit_reporte(actor_user, reporte)
        and reporte.estado in (ReportStatus.draft, ReportStatus.needs_changes)
    )


def get_allowed_actions_for_reporte(actor_user: User, reporte: Reporte) -> list[str]:
    actions: list[str] = []

    if can_edit_report(actor_user, reporte):
        actions.extend(["edit_header", "save_detail", "submit"])

    if can_review_reporte(actor_user, reporte):
        if reporte.estado == ReportStatus.submitted:
            actions.append("start_review")
        if reporte.estado == ReportStatus.under_review:
            actions.extend(["approve", "reject"])

    if can_reopen_reporte(actor_user, reporte):
        if reporte.estado == ReportStatus.approved:
            actions.append("reopen")

    return actions

def ensure_can_edit(actor_user: User, reporte: Reporte) -> None:
    if not can_read_reporte(actor_user, reporte):
        raise BusinessRuleError("Reporte no existe o no pertenece a tu empresa.", 404)
    if actor_user.empresa_id != reporte.empresa_id:
        raise BusinessRuleError("No puedes editar reportes de otra empresa.", 403)
    if not can_create_or_edit_reporte(actor_user, reporte):
        raise BusinessRuleError("Solo un evaluador/admin puede editar reportes.", 403)

def ensure_reporte_editable_by_evaluador(reporte: Reporte) -> None:
    """
    El evaluador puede editar si:
    - estado = draft
    - estado = needs_changes
    """
    if reporte.estado not in (ReportStatus.draft, ReportStatus.needs_changes):
        raise BusinessRuleError("Este reporte ya no se puede editar (ya fue enviado o está bloqueado).")
    
def ensure_productor_valid_for_empresa(db: Session,empresa_id: int,productor_id: int | None) -> None:
    # 1 Verificar empresa
    empresa = db.get(Empresa, empresa_id)
    if empresa is None:
        raise BusinessRuleError("La empresa no existe.")

    # 2 Si productor es opcional
    if productor_id is None:
        return

    # 3 Verificar productor
    productor = db.get(Productor, productor_id)
    if productor is None:
        raise BusinessRuleError("El productor no existe.")

    # 4 Verificar pertenencia empresa-productor
    if productor.empresa_id != empresa_id:
        raise BusinessRuleError(
            "El productor no pertenece a la empresa indicada."
        )     
    

def apply_productor_change(db: Session, reporte: Reporte, new_productor_id: int) -> None:
    """
    Cambiar productor implica:
    - actualizar automaticamente el combobox de las haciendas
    - borrar la hacienda si ya había sido escogida
    """
    reporte.productor_id = new_productor_id
    reporte.hacienda_id = None

def apply_hacienda_change(db: Session, reporte: Reporte, new_hacienda_id: int ) -> None:

    """
    Validaremos que la hacienda exista, que antes de seleccionarla elija a un productor
    Que no pueda seleccionar una hacienda de otra empresa
    Que la hacienda pertenezca al productor seleccionado

    """
    hac = db.get(Hacienda, new_hacienda_id)

    if not hac:
        raise BusinessRuleError("La hacienda indicada no existe.")

    if hac.empresa_id != reporte.empresa_id:
        raise BusinessRuleError("No puedes usar una hacienda de otra empresa.")

    if reporte.productor_id is None:
        raise BusinessRuleError("Primero selecciona un productor.")

    if hac.productor_id != reporte.productor_id:
        raise BusinessRuleError("Esa hacienda no pertenece al productor seleccionado.")

    reporte.hacienda_id = hac.id

def ensure_reporte_refs_consistent(db: Session, reporte: Reporte) -> None:
    if reporte.productor_id is not None:
        ensure_productor_valid_for_empresa(db, reporte.empresa_id, reporte.productor_id)

    if reporte.hacienda_id is not None:
        hac = db.get(Hacienda, reporte.hacienda_id)
        if not hac:
            raise BusinessRuleError("La hacienda indicada no existe.")
        if hac.empresa_id != reporte.empresa_id:
            raise BusinessRuleError("Hacienda no pertenece a la empresa.")
        if reporte.productor_id is not None and hac.productor_id != reporte.productor_id:
            raise BusinessRuleError("Hacienda no pertenece al productor seleccionado.")


def create_draft(db: Session, data: ReporteCreateDraft, actor_user: User) -> Reporte:
    if not can_create_or_edit_reporte(actor_user):
        raise BusinessRuleError("Solo un evaluador/admin puede crear reportes.", 403)

    payload = data.model_copy(update={"empresa_id": actor_user.empresa_id})
    return reporte_crud.create_draft(db, payload, empresa_id=actor_user.empresa_id,created_by_user_id=actor_user.id)

def update_draft(db: Session, reporte: Reporte, patch: ReporteUpdateDraft, actor_user: User) -> Reporte:
    """
    Actualiza un draft con reglas de negocio.
    - Valida si está editable
    - Si cambia productor_id: valida y recalcula hacienda_id
    - Actualiza semana_reporte/fecha_reporte si vienen
    """
    ensure_can_edit(actor_user, reporte)
    ensure_reporte_editable_by_evaluador(reporte)

    #exclude_unset=True solo toma los campos que el cliente realmente mandó.
    data = patch.model_dump(exclude_unset=True)

    # 1) Si viene productor_id, aplicar regla especial
    if "productor_id" in data and data["productor_id"] is not None:
        ensure_productor_valid_for_empresa(db, reporte.empresa_id, data["productor_id"])
        apply_productor_change(db, reporte, data.pop("productor_id"))

    if "hacienda_id" in data and data["hacienda_id"] is not None:
        apply_hacienda_change(db, reporte, data.pop("hacienda_id"))

    for k, v in data.items():
        setattr(reporte, k, v)

    return reporte_crud.save(db, reporte)


################################################
#                                              #
#       VALIDACIONES PARA SUBMIT REPORTE       #
#                                              #
################################################

REQUIRED_HEADER_FIELDS = [
    "productor_id",
    "hacienda_id",
    "semana_reporte",
    "fecha_reporte",
    "tipo"
]

REQUIRED_BY_TYPE = {
    ReportType.reporte_de_gancho: [
        ("gancho_detalle", None),  # debe existir
    ],
    ReportType.terminados_de_proceso: [
        ("terminado_detalle", None),
    ],
}

def ensure_gancho_ready_to_submit(reporte: Reporte) -> None:
    if reporte.gancho_detalle is None:
        raise BusinessRuleError("Falta el detalle de gancho.")

    rp = reporte.gancho_detalle.racimos_procesados
    if rp is None or rp <= 0:
        raise BusinessRuleError("racimos_procesados debe ser mayor que 0 para enviar el reporte de gancho.")

    # Si hay cintas, exigir cantidad y color
    for idx, cinta in enumerate(reporte.gancho_cintas, start=1):
        if cinta.color_id is None:
            raise BusinessRuleError(f"En cintas: falta color_id en el item #{idx}.")
        if cinta.cantidad is None or cinta.cantidad <= 0:
            raise BusinessRuleError(f"En cintas: cantidad debe ser > 0 en el item #{idx}.")
        
def ensure_terminado_ready_to_submit(reporte: Reporte) -> None:
    if reporte.terminado_detalle is None:
        raise BusinessRuleError("Falta el detalle de terminado.")

    if reporte.terminado_detalle.total_cajas is None or reporte.terminado_detalle.total_cajas <= 0:
        raise BusinessRuleError("El total de cajas debe ser mayor que 0 para enviar el terminado.")

    lotes = list(reporte.terminado_detalle.lotes or [])
    if len(lotes) == 0:
        raise BusinessRuleError("Debes registrar al menos 1 lote para enviar el terminado.")

    for i, lote in enumerate(lotes, start=1):
        marcas = list(lote.marcas or [])
        if len(marcas) == 0:
            raise BusinessRuleError(f"El lote #{i} no tiene marcas registradas.")

        for j, marca in enumerate(marcas, start=1):
            if marca.cajas is None or marca.cajas <= 0:
                raise BusinessRuleError(f"En lote #{i}, marca #{j}: cajas debe ser > 0.")


def validate_racimos(num_racim: int | None) -> None:
    if num_racim is None or num_racim <= 0:
        raise BusinessRuleError("La cantidad de racimos procesados debe ser mayor que 0.")


def validate_required_fields (obj, fields:list [str]) -> None:
    missing= [f for f in fields if getattr(obj, f) in (None, "", [])]
    if missing:
        raise BusinessRuleError(f"Faltan campos obligatorios para enviar: {', '.join(missing)}")


def submit_reporte(db: Session, reporte: Reporte, actor_user: User) -> Reporte:
    ensure_can_edit(actor_user, reporte)

    if reporte.estado not in (ReportStatus.draft, ReportStatus.needs_changes):
        raise BusinessRuleError("Este reporte no está en un estado enviable.")

    validate_required_fields(reporte, REQUIRED_HEADER_FIELDS)
    ensure_reporte_refs_consistent(db, reporte)

    if reporte.tipo == ReportType.reporte_de_gancho:
        ensure_gancho_ready_to_submit(reporte)

    elif reporte.tipo == ReportType.terminados_de_proceso:
        ensure_terminado_ready_to_submit(reporte)

    from_status = reporte.estado
    reporte.estado = ReportStatus.submitted
    reporte.submitted_at = datetime.now(timezone.utc)

    revision = make_revision(
        reporte=reporte,
        actor_user=actor_user,
        from_status=from_status,
        to_status=ReportStatus.submitted,
        comentario="Reporte enviado a revision.",
    )
    return reporte_crud.save_with_revision(db, reporte, revision)

#Función para traer los reportes en lsita y poder revisarlos

def review_reporte(db: Session, reporte: Reporte, payload: ReporteReview, actor_user: User) -> Reporte:
    if not can_review_reporte(actor_user, reporte):
        raise BusinessRuleError("Solo un supervisor/admin puede revisar reportes.", 403)

    if reporte.estado != ReportStatus.under_review:
        raise BusinessRuleError("Solo se pueden revisar reportes que están en revisión.")

    from_status = reporte.estado

    if payload.accion == "aprobado":
        to_status = ReportStatus.approved
    elif payload.accion == "rechazado":
        to_status = ReportStatus.needs_changes
    else:
        raise BusinessRuleError("Acción de revisión inválida.")

    reporte.estado = to_status

    revision = make_revision(reporte, actor_user, from_status, to_status, payload.comentario)
    return reporte_crud.save_with_revision(db, reporte, revision)

def list_reportes(
    db: Session,
    actor_user: User,
    estado: ReportStatus | None = None,
    tipo: ReportType | None = None,
    semana_reporte: int | None = None,
    productor_id: int | None = None,
    hacienda_id: int | None = None,
    fecha_desde: date | None = None,
    fecha_hasta: date | None = None,
    limit: int = 20,
    offset: int = 0,
    search: str | None = None,
    order_by: str | None = None,
    order_dir: str | None = "desc",
):
    if fecha_desde and fecha_hasta and fecha_desde > fecha_hasta:
        raise BusinessRuleError("fecha_desde no puede ser mayor que fecha_hasta")

    allowed_order_fields = ["fecha_reporte", "semana_reporte", "id"]

    if order_by and order_by not in allowed_order_fields:
        raise BusinessRuleError("Campo de orden inválido")

    if order_dir not in ["asc", "desc"]:
        raise BusinessRuleError("Dirección de orden inválida")

    created_by_user_id = actor_user.id if actor_user.role == "evaluador" else None

    total, items = reporte_crud.crud_list_reportes(
        db=db,
        empresa_id=actor_user.empresa_id,
        created_by_user_id=created_by_user_id,
        estado=estado,
        tipo=tipo,
        semana_reporte=semana_reporte,
        productor_id=productor_id,
        hacienda_id=hacienda_id,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        limit=limit,
        offset=offset,
        search=search,
        order_by=order_by,
        order_dir=order_dir,
    )

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": items,
    }

def get_reporte_detail(db: Session, reporte_id: int, actor_user: User) -> Reporte:
    reporte = reporte_crud.get_detail(
        db=db,
        reporte_id=reporte_id,
        empresa_id=actor_user.empresa_id,
    )

    if reporte is None:
        raise BusinessRuleError("Reporte no existe o no pertenece a tu empresa.", 404)

    if not can_read_reporte(actor_user, reporte):
        raise BusinessRuleError("Reporte no existe o no pertenece a tu empresa.", 404)

    reporte.allowed_actions = get_allowed_actions_for_reporte(actor_user, reporte)
    return reporte


def start_review(db: Session, reporte: Reporte, actor_user: User) -> Reporte:
    if not can_review_reporte(actor_user, reporte):
        raise BusinessRuleError("Solo un supervisor/admin puede iniciar revisión.", 403)

    if reporte.estado != ReportStatus.submitted:
        raise BusinessRuleError("Solo se pueden tomar reportes enviados.")

    from_status = reporte.estado
    reporte.estado = ReportStatus.under_review
    reporte.supervisor_id = actor_user.id

    revision = make_revision(
        reporte=reporte,
        actor_user=actor_user,
        from_status=from_status,
        to_status=ReportStatus.under_review,
        comentario="Revision iniciada.",
    )
    return reporte_crud.save_with_revision(db, reporte, revision)


def reopen_reporte(db: Session, reporte: Reporte, payload: ReporteReopen, actor_user: User) -> Reporte:
    if not can_reopen_reporte(actor_user, reporte):
        raise BusinessRuleError("Solo un admin puede reabrir reportes.", 403)

    if reporte.estado != ReportStatus.approved:
        raise BusinessRuleError("Solo se pueden reabrir reportes aprobados.")

    comentario = payload.comentario.strip()
    if not comentario:
        raise BusinessRuleError("El comentario es obligatorio para reabrir.")

    from_status = reporte.estado
    reporte.estado = ReportStatus.needs_changes
    reporte.supervisor_id = None
    reporte.submitted_at = None

    revision = make_revision(
        reporte=reporte,
        actor_user=actor_user,
        from_status=from_status,
        to_status=ReportStatus.needs_changes,
        comentario=comentario,
    )
    return reporte_crud.save_with_revision(db, reporte, revision)
