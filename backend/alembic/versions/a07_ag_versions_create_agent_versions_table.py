"""create agent versions table

Revision ID: a07_ag_versions
Revises: a06_agents
Create Date: 2026-08-17 22:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a07_ag_versions'
down_revision: Union[str, Sequence[str], None] = 'a06_agents'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('agent_versions',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('agent_id', sa.UUID(), nullable=False),
    sa.Column('version_number', sa.Integer(), nullable=False),
    sa.Column('instructions', sa.Text(), nullable=False),
    sa.Column('model', sa.String(length=255), nullable=True),
    sa.Column('temperature', sa.Float(), nullable=True),
    sa.Column('configuration', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('created_by', sa.UUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('agent_id', 'version_number', name='uq_agent_version')
    )
    op.create_index(op.f('ix_agent_versions_agent_id'), 'agent_versions', ['agent_id'], unique=False)
    op.create_index(op.f('ix_agent_versions_created_by'), 'agent_versions', ['created_by'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_agent_versions_created_by'), table_name='agent_versions')
    op.drop_index(op.f('ix_agent_versions_agent_id'), table_name='agent_versions')
    op.drop_table('agent_versions')
