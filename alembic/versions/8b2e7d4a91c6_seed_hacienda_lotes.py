"""seed hacienda lotes

Revision ID: 8b2e7d4a91c6
Revises: 6a8d2c9f4b13
Create Date: 2026-05-28 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "8b2e7d4a91c6"
down_revision: Union[str, None] = "6a8d2c9f4b13"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


LOTES = [1, 2, 3, 4, 5]


def upgrade() -> None:
    for numero_lote in LOTES:
        op.execute(
            f"""
            INSERT INTO hacienda_lotes (hacienda_id, numero_lote, created_at, updated_at)
            SELECT id, {numero_lote}, NOW(), NOW()
            FROM haciendas
            WHERE NOT EXISTS (
                SELECT 1
                FROM hacienda_lotes
                WHERE hacienda_lotes.hacienda_id = haciendas.id
                AND hacienda_lotes.numero_lote = {numero_lote}
            )
            """
        )


def downgrade() -> None:
    numeros = ", ".join(str(numero_lote) for numero_lote in LOTES)
    op.execute(f"DELETE FROM hacienda_lotes WHERE numero_lote IN ({numeros})")
