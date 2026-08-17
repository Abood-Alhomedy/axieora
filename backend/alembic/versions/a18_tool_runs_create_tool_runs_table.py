"""create tool runs table

Revision ID: a18_tool_runs
Revises: a17_agent_runs
Create Date: 2026-08-17 22:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a18_tool_runs'
down_revision: Union[str, Sequence[str], None] = 'a17_agent_runs'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('tool_runs',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('agent_run_id', sa.UUID(), nullable=False),
    sa.Column('tool_id', sa.UUID(), nullable=False),
    sa.Column('input', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('output', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('error_message', sa.Text(), nullable=True),
    sa.Column('duration_ms', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['agent_run_id'], ['agent_runs.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tool_id'], ['tools.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tool_runs_agent_run_id'), 'tool_runs', ['agent_run_id'], unique=False)
    op.create_index(op.f('ix_tool_runs_tool_id'), 'tool_runs', ['tool_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_tool_runs_tool_id'), table_name='tool_runs')
    op.drop_index(op.f('ix_tool_runs_agent_run_id'), table_name='tool_runs')
    op.drop_table('tool_runs')
