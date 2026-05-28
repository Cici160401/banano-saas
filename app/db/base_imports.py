# backend/app/db/base_imports.py

# === Core models ===
from app.models.empresa import Empresa
from app.models.user import User
from app.models.productor import Productor
from app.models.hacienda import Hacienda

# === Reportes ===
from app.models.reporte import Reporte
from app.models.reporte_revision import ReporteRevision
from app.models.reporte_gancho_cinta import ReporteGanchoCinta
from app.models.reporte_gancho_detalle import ReporteGanchoDetalle
from app.models.reporte_gancho_motivos import ReporteGanchoMotivo

# === Calendario ===
from app.models.calendario_enfunde import CalendarioEnfunde
from app.models.calendario_enfunde_item import CalendarioEnfundeItem

# === Terminados ===
from app.models.terminado_lotes import TerminadoLote
from app.models.terminado_lote_marca import TerminadoLoteMarca
from app.models.terminado_marca import TerminadoMarca
from app.models.terminado_proceso_detalle import TerminadoProcesoDetalle

# === Otros ===
from app.models.refresh_token import RefreshToken
from app.models.cinta_color import CintaColor
from app.models.marca import Marca
from app.models.motivo_gancho import MotivoGancho

# Nota:
# No importamos mixins ni enum porque no son tablas.
