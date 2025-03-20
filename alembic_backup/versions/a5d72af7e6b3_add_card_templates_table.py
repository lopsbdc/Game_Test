"""add_card_templates_table
Revision ID: 3311424c5308
Revises: 98fa7682ca3e
Create Date: 2025-03-20 11:42:05.139088
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

# revision identifiers, used by Alembic.
revision: str = 'a5d72af7e6b3'
down_revision: Union[str, None] = '98fa7682ca3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('card_templates',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('background_type', sa.String(), server_default="color_based"),
        sa.Column('overlay_opacity', sa.Integer(), server_default="80"),
        sa.Column('width_mm', sa.Integer(), server_default="63"),
        sa.Column('height_mm', sa.Integer(), server_default="88"),
        sa.Column('zones', JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('card_templates')