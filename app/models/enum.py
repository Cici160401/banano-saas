from enum import Enum

class UserRole(str, Enum):
    evaluador = "evaluador"
    supervisor = "supervisor"
    admin = "admin"  #un admin de empresa

class ReportType(str, Enum):
    reporte_de_gancho = "reporte_de_gancho"
    terminados_de_proceso = "terminados_de_proceso"

class ReportStatus(str, Enum):
    draft = "draft"                # borrador (solo evaluador)
    submitted = "submitted"        # enviado al supervisor
    needs_changes = "needs_changes"  # supervisor pide cambios
    approved = "approved"          # aprobado
    #rejected = "rejected"          # rechazado definitivo (opcional)
    under_review = "under_review"  #bajo revisión

class ReportAction(str, Enum):
    created = "created"            #reporte creado          
    saved_draft = "saved_draft"    #borrador guardado
    submitted = "submitted"        #reporte enviado
    needs_changes = "needs_changes"#se necesitan cambios (reporte previamente rechazado)
    resubmitted = "resubmitted"    #reporte re-enviado
    approved = "approved"          #reporte aprovdo
    #rejected = "rejected"          #reporte rechazado

