"""create workflow run steps table

Revision ID: a20_wf_steps
Revises: a19_wf_runs
Create Date: 2026-08-17 22:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a20_wf_steps'
down_revision: Union[str, Sequence[str], None] = 'a19_wf_runs'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('workflow_run_steps',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('workflow_run_id', sa.UUID(), nullable=False),
    sa.Column('node_id', sa.UUID(), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('input_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('output_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('error_message', sa.Text(), nullable=True),
    sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('duration_ms', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['node_id'], ['workflow_nodes.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['workflow_run_id'], ['workflow_runs.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workflow_run_steps_node_id'), 'workflow_run_steps', ['node_id'], unique=False)
    op.create_index(op.f('ix_workflow_run_steps_workflow_run_id'), 'workflow_run_steps', ['workflow_run_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_workflow_run_steps_workflow_run_id'), table_name='workflow_run_steps')
    op.drop_index(op.f('ix_workflow_run_steps_node_id'), table_name='workflow_run_steps')
    op.drop_table('workflow_run_steps')
