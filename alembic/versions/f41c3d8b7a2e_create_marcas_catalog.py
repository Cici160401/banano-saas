"""create marcas catalog

Revision ID: f41c3d8b7a2e
Revises: d729c787be50
Create Date: 2026-05-28 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f41c3d8b7a2e"
down_revision: Union[str, None] = "d729c787be50"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "marcas",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("empresa_id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=150), nullable=False),
        sa.Column("activo", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("orden", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["empresa_id"], ["empresas.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("empresa_id", "nombre", name="uq_marca_empresa_nombre"),
    )
    op.create_index(op.f("ix_marcas_empresa_id"), "marcas", ["empresa_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_marcas_empresa_id"), table_name="marcas")
    op.drop_table("marcas")
