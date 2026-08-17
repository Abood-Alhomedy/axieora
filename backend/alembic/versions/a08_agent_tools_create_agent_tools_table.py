"""create agent tools table

Revision ID: a08_agent_tools
Revises: a07_ag_versions
Create Date: 2026-08-17 22:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a08_agent_tools'
down_revision: Union[str, Sequence[str], None] = 'a07_ag_versions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('agent_tools',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('agent_id', sa.UUID(), nullable=False),
    sa.Column('tool_id', sa.UUID(), nullable=False),
    sa.Column('configuration', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tool_id'], ['tools.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('agent_id', 'tool_id', name='uq_agent_tool')
    )
    op.create_index(op.f('ix_agent_tools_agent_id'), 'agent_tools', ['agent_id'], unique=False)
    op.create_index(op.f('ix_agent_tools_tool_id'), 'agent_tools', ['tool_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_agent_tools_tool_id'), table_name='agent_tools')
    op.drop_index(op.f('ix_agent_tools_agent_id'), table_name='agent_tools')
    op.drop_table('agent_tools')
