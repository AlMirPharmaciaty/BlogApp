"""adding roles to users

Revision ID: 97681e42ca4f
Revises: 43dc1b5a8fbe
Create Date: 2024-07-22 14:49:14.009310

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "97681e42ca4f"
down_revision: Union[str, None] = "43dc1b5a8fbe"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("roles", sa.ARRAY(sa.String)))


def downgrade() -> None:
    pass
