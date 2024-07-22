"""updating blogs table

Revision ID: 572ad59e934e
Revises: 0096b78600d2
Create Date: 2024-07-22 13:39:57.040068

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '572ad59e934e'
down_revision: Union[str, None] = '0096b78600d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
