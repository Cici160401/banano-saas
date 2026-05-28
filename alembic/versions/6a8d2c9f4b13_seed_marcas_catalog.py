"""seed marcas catalog

Revision ID: 6a8d2c9f4b13
Revises: f41c3d8b7a2e
Create Date: 2026-05-28 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "6a8d2c9f4b13"
down_revision: Union[str, None] = "f41c3d8b7a2e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


MARCAS = [
    ("Banana Prime", 1),
    ("Tropical Gold", 2),
    ("Costa Verde", 3),
    ("EcoBanano", 4),
    ("Sol del Agro", 5),
]


def upgrade() -> None:
    for nombre, orden in MARCAS:
        op.execute(
            f"""
            INSERT INTO marcas (empresa_id, nombre, activo, orden, created_at, updated_at)
            SELECT id, '{nombre}', 1, {orden}, NOW(), NOW()
            FROM empresas
            WHERE NOT EXISTS (
                SELECT 1
                FROM marcas
                WHERE marcas.empresa_id = empresas.id
                AND marcas.nombre = '{nombre}'
            )
            """
        )


def downgrade() -> None:
    nombres = "', '".join(nombre for nombre, _orden in MARCAS)
    op.execute(f"DELETE FROM marcas WHERE nombre IN ('{nombres}')")
