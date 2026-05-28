from app.models.enum import UserRole
from app.models.reporte import Reporte
from app.models.user import User


def has_role(user: User, *roles: UserRole) -> bool:
    return user.role in roles


def same_empresa(user: User, empresa_id: int) -> bool:
    return user.empresa_id == empresa_id


def can_read_reporte(user: User, reporte: Reporte) -> bool:
    if not same_empresa(user, reporte.empresa_id):
        return False

    if has_role(user, UserRole.admin, UserRole.supervisor):
        return True

    return has_role(user, UserRole.evaluador) and reporte.created_by_user_id == user.id


def can_create_or_edit_reporte(user: User, reporte: Reporte | None = None) -> bool:
    if not has_role(user, UserRole.admin, UserRole.evaluador):
        return False

    if reporte is None:
        return True

    if not same_empresa(user, reporte.empresa_id):
        return False

    if has_role(user, UserRole.admin):
        return True

    return reporte.created_by_user_id == user.id


def can_review_reporte(user: User, reporte: Reporte) -> bool:
    return same_empresa(user, reporte.empresa_id) and has_role(
        user,
        UserRole.admin,
        UserRole.supervisor,
    )


def can_reopen_reporte(user: User, reporte: Reporte) -> bool:
    return same_empresa(user, reporte.empresa_id) and has_role(user, UserRole.admin)
