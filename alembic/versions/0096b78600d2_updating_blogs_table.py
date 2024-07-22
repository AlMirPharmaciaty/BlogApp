"""updating blogs table

Revision ID: 0096b78600d2
Revises: ff0b9a2ac43d
Create Date: 2024-07-22 13:28:09.042101

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0096b78600d2'
down_revision: Union[str, None] = 'ff0b9a2ac43d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
