"""adding roles to users

Revision ID: 43dc1b5a8fbe
Revises: 572ad59e934e
Create Date: 2024-07-22 14:46:58.031751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43dc1b5a8fbe'
down_revision: Union[str, None] = '572ad59e934e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
