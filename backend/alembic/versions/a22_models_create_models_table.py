"""create models table

Revision ID: a22_models
Revises: a21_mod_provs
Create Date: 2026-08-17 22:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a22_models'
down_revision: Union[str, Sequence[str], None] = 'a21_mod_provs'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('models',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('provider_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('slug', sa.String(length=255), nullable=False),
    sa.Column('context_window', sa.Integer(), nullable=True),
    sa.Column('input_price', sa.Float(), nullable=True),
    sa.Column('output_price', sa.Float(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['provider_id'], ['model_providers.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('provider_id', 'slug', name='uq_provider_model_slug')
    )
    op.create_index(op.f('ix_models_provider_id'), 'models', ['provider_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_models_provider_id'), table_name='models')
    op.drop_table('models')
