from sqlalchemy.orm import Session, selectinload
from app.models.reporte import Reporte
from app.models.reporte_gancho_detalle import ReporteGanchoDetalle
from app.models.reporte_gancho_cinta import ReporteGanchoCinta
from app.models.reporte_gancho_motivos import ReporteGanchoMotivo
from app.models.reporte_revision import ReporteRevision
from app.models.terminado_lotes import TerminadoLote
from app.models.terminado_proceso_detalle import TerminadoProcesoDetalle
from app.schemas.reporte import ReporteCreateDraft, ReporteUpdateDraft
from app.models.enum import ReportStatus
from decimal import Decimal
from sqlalchemy import or_
from app.models.productor import Productor
from app.models.hacienda import Hacienda
from sqlalchemy import asc, desc
#El evaluador crea un draft (puede estar incompleto).
#Lo puede ir editando.
#Cuando lo envía (submit): se bloquea para el evaluador.
#Si el supervisor pide cambios (needs_changes): vuelve a ser editable por el evaluador.
#Quitamos rejected (ok, más simple).

# Todo lo que venga después del * debe pasarse como argumento nombrado (keyword argument).

#FUNCION DE GUARDAR GENERAL
def save(db: Session, obj: Reporte) -> Reporte:
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

#FUNCION DE GUARDAR REPORTE Y REVISION
def save_with_revision(
    db: Session,
    reporte: Reporte,
    revision: ReporteRevision,
) -> Reporte:
    db.add(reporte)
    db.add(revision)
    db.commit()
    db.refresh(reporte)
    return reporte


def create_draft(db: Session, data: ReporteCreateDraft, *, empresa_id: int, created_by_user_id: int) -> Reporte:
    """
    Crea el header del reporte en estado draft.
    Puede venir incompleto (hacienda/productor/semana/fecha pueden ser None).
    """
    obj = Reporte(
        empresa_id=empresa_id,                 # obligatorio (multi-tenant)
        hacienda_id=data.hacienda_id,               # puede ser None
        productor_id=data.productor_id,             # puede ser None
        tipo=data.tipo,                             # obligatorio
        semana_reporte=data.semana_reporte,         # puede ser None
        fecha_reporte=data.fecha_reporte,           # puede ser None
        created_by_user_id=created_by_user_id,      # obligatorio (quién lo creó)
        estado=ReportStatus.draft,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get(db: Session, reporte_id: int) -> Reporte | None:
    return db.get(Reporte, reporte_id)

def update_draft_fields(db: Session, obj: Reporte, patch: ReporteUpdateDraft) -> Reporte:
    #exclude_unset=True solo toma los campos que el cliente realmente mandó.
    data = patch.model_dump(exclude_unset=True)   
    
    ## QUE ES LO QUE SUCEDE AQUI?    
    #CON EL METODO SETATTR LO QUE HACEMOS ES DECIRLE, DEL OBJETO OBJ, SU ATRIBUTO K, AHORA TIENE EL VALOR DE V.
    
    data = patch.model_dump(exclude_unset=True)

    for k, v in data.items():
        setattr(obj, k, v)

    return save(db, obj)

def crud_list_reportes(
    db: Session,
    empresa_id: int,
    created_by_user_id=None,
    estado=None,
    tipo=None,
    semana_reporte=None,
    productor_id=None,
    hacienda_id=None,
    fecha_desde=None,
    fecha_hasta=None,
    limit=20,
    offset=0,
    search: str | None = None,
    order_by: str | None = None,
    order_dir: str = "desc",
):
    query = (
        db.query(Reporte)
        .options(
            selectinload(Reporte.productor),
            selectinload(Reporte.hacienda),
            selectinload(Reporte.created_by),
        )
        .filter(Reporte.empresa_id == empresa_id)
    )

    if estado is not None:
        query = query.filter(Reporte.estado == estado)

    if created_by_user_id is not None:
        query = query.filter(Reporte.created_by_user_id == created_by_user_id)

    if tipo is not None:
        query = query.filter(Reporte.tipo == tipo)

    if semana_reporte is not None:
        query = query.filter(Reporte.semana_reporte == semana_reporte)

    if productor_id is not None:
        query = query.filter(Reporte.productor_id == productor_id)

    if hacienda_id is not None:
        query = query.filter(Reporte.hacienda_id == hacienda_id)

    if fecha_desde is not None:
        query = query.filter(Reporte.fecha_reporte >= fecha_desde)

    if fecha_hasta is not None:
        query = query.filter(Reporte.fecha_reporte <= fecha_hasta)

    if search:
        query = query.join(Productor, isouter=True).join(Hacienda, isouter=True)

        query = query.filter(
            or_(
                Productor.nombre.ilike(f"%{search}%"),
                Hacienda.nombre.ilike(f"%{search}%"),
            )
        )

    # ✅ ORDENAMIENTO SEGURO
    ALLOWED_ORDER_FIELDS = {
        "id": Reporte.id,
        "fecha_reporte": Reporte.fecha_reporte,
        "semana_reporte": Reporte.semana_reporte,
    }

    if order_by in ALLOWED_ORDER_FIELDS:
        column = ALLOWED_ORDER_FIELDS[order_by]

        if order_dir == "asc":
            query = query.order_by(asc(column))
        else:
            query = query.order_by(desc(column))
    else:
        query = query.order_by(Reporte.id.desc())

    total = query.count()

    items = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return total, items

def get_detail(
    db: Session,
    reporte_id: int,
    empresa_id: int,
) -> Reporte | None:
    return (
        db.query(Reporte)
        .options(
            selectinload(Reporte.empresa),
            selectinload(Reporte.productor),
            selectinload(Reporte.hacienda),
            selectinload(Reporte.created_by),
            selectinload(Reporte.supervisor),
            selectinload(Reporte.gancho_detalle),
            selectinload(Reporte.gancho_cintas).selectinload(ReporteGanchoCinta.color),
            selectinload(Reporte.gancho_motivos).selectinload(ReporteGanchoMotivo.motivo),
            selectinload(Reporte.terminado_detalle)
            .selectinload(TerminadoProcesoDetalle.lotes)
            .selectinload(TerminadoLote.marcas),
            selectinload(Reporte.historial).selectinload(ReporteRevision.actor),
        )
        .filter(
            Reporte.id == reporte_id,
            Reporte.empresa_id == empresa_id,
        )
        .first()
    )

