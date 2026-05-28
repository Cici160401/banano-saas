"""fix haciendas id autoincrement

Revision ID: 4c0f8d2a6e91
Revises: 9d5a7c1b2e04
Create Date: 2026-05-28 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "4c0f8d2a6e91"
down_revision: Union[str, None] = "9d5a7c1b2e04"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("reportes_ibfk_3", "reportes", type_="foreignkey")
    op.drop_constraint("hacienda_lotes_ibfk_1", "hacienda_lotes", type_="foreignkey")
    op.execute("ALTER TABLE haciendas MODIFY id INT NOT NULL AUTO_INCREMENT")
    op.create_foreign_key(
        "reportes_ibfk_3",
        "reportes",
        "haciendas",
        ["hacienda_id"],
        ["id"],
    )
    op.create_foreign_key(
        "hacienda_lotes_ibfk_1",
        "hacienda_lotes",
        "haciendas",
        ["hacienda_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint("reportes_ibfk_3", "reportes", type_="foreignkey")
    op.drop_constraint("hacienda_lotes_ibfk_1", "hacienda_lotes", type_="foreignkey")
    op.execute("ALTER TABLE haciendas MODIFY id INT NOT NULL")
    op.create_foreign_key(
        "reportes_ibfk_3",
        "reportes",
        "haciendas",
        ["hacienda_id"],
        ["id"],
    )
    op.create_foreign_key(
        "hacienda_lotes_ibfk_1",
        "hacienda_lotes",
        "haciendas",
        ["hacienda_id"],
        ["id"],
    )
