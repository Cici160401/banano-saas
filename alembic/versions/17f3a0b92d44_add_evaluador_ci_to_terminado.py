"""add identificacion fields for terminado evaluator

Revision ID: 17f3a0b92d44
Revises: 8b2e7d4a91c6
Create Date: 2026-05-28 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "17f3a0b92d44"
down_revision: Union[str, None] = "8b2e7d4a91c6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("identificacion", sa.String(length=50), nullable=True),
    )
    op.add_column(
        "terminado_proceso_detalles",
        sa.Column("evaluador_ci", sa.String(length=30), nullable=True),
    )
    op.execute(
        """
        UPDATE users
        SET identificacion = '0703951905'
        WHERE email = 'admin@test.com'
        AND identificacion IS NULL
        """
    )


def downgrade() -> None:
    op.drop_column("terminado_proceso_detalles", "evaluador_ci")
    op.drop_column("users", "identificacion")
