"""seed frontend test data

Revision ID: 9d5a7c1b2e04
Revises: 17f3a0b92d44
Create Date: 2026-05-28 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "9d5a7c1b2e04"
down_revision: Union[str, None] = "17f3a0b92d44"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


PASSWORD_HASH = "$2b$12$UxNj0MwDF9kWfjXwMC.Ny.m7hNLY.AKrv2Cn1Lky7m9p4D6oq30VS"


def upgrade() -> None:
    op.execute(
        f"""
        INSERT INTO users (
            empresa_id, nombre, identificacion, email, password_hash, role,
            is_active, created_at, updated_at
        )
        SELECT 1, 'Evaluador Test', '0911111111', 'evaluador@test.com',
               '{PASSWORD_HASH}', 'evaluador', 1, NOW(), NOW()
        WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'evaluador@test.com')
        """
    )
    op.execute(
        f"""
        INSERT INTO users (
            empresa_id, nombre, identificacion, email, password_hash, role,
            is_active, created_at, updated_at
        )
        SELECT 1, 'Supervisor Test', '0922222222', 'supervisor@test.com',
               '{PASSWORD_HASH}', 'supervisor', 1, NOW(), NOW()
        WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'supervisor@test.com')
        """
    )
    op.execute(
        """
        INSERT INTO productores (
            empresa_id, codigo_productor, nombre, identificacion, telefono,
            created_at, updated_at
        )
        SELECT 1, 1001, 'Productor Demo', '0999999999', '0990000000', NOW(), NOW()
        WHERE NOT EXISTS (
            SELECT 1 FROM productores
            WHERE empresa_id = 1 AND codigo_productor = 1001
        )
        """
    )
    op.execute(
        """
        INSERT INTO haciendas (
            id, empresa_id, productor_id, codigo_hacienda, nombre, zona, direccion,
            hectareas, created_at, updated_at
        )
        SELECT COALESCE((SELECT MAX(h2.id) + 1 FROM haciendas h2), 1),
               1, p.id, 2001, 'Hacienda Demo', 'Zona Demo', 'Direccion demo',
               10, NOW(), NOW()
        FROM productores p
        WHERE p.empresa_id = 1
        AND p.codigo_productor = 1001
        AND NOT EXISTS (
            SELECT 1 FROM haciendas
            WHERE empresa_id = 1 AND codigo_hacienda = 2001
        )
        """
    )
    for numero_lote in (1, 2, 3, 4, 5):
        op.execute(
            f"""
            INSERT INTO hacienda_lotes (hacienda_id, numero_lote, created_at, updated_at)
            SELECT h.id, {numero_lote}, NOW(), NOW()
            FROM haciendas h
            WHERE h.empresa_id = 1
            AND h.codigo_hacienda = 2001
            AND NOT EXISTS (
                SELECT 1 FROM hacienda_lotes
                WHERE hacienda_id = h.id AND numero_lote = {numero_lote}
            )
            """
        )


def downgrade() -> None:
    op.execute(
        """
        DELETE hl FROM hacienda_lotes hl
        JOIN haciendas h ON h.id = hl.hacienda_id
        WHERE h.empresa_id = 1 AND h.codigo_hacienda = 2001
        """
    )
    op.execute("DELETE FROM haciendas WHERE empresa_id = 1 AND codigo_hacienda = 2001")
    op.execute("DELETE FROM productores WHERE empresa_id = 1 AND codigo_productor = 1001")
    op.execute("DELETE FROM users WHERE email IN ('evaluador@test.com', 'supervisor@test.com')")
