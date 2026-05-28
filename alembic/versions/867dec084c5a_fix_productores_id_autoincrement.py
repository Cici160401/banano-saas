"""fix productores id autoincrement

Revision ID: 867dec084c5a
Revises: 1026cda1397d
Create Date: 2026-02-26 19:44:20.768636

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '867dec084c5a'
down_revision: Union[str, None] = '1026cda1397d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE productores MODIFY id INT NOT NULL AUTO_INCREMENT")


def downgrade() -> None:
    op.execute("ALTER TABLE productores MODIFY id INT NOT NULL")
