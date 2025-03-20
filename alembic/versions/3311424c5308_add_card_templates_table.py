"""add_card_templates_table

Revision ID: 3311424c5308
Revises: 98fa7682ca3e
Create Date: 2025-03-20 11:42:05.139088

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3311424c5308'
down_revision: Union[str, None] = '98fa7682ca3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
