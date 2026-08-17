"""create workflow runs table

Revision ID: a19_wf_runs
Revises: a18_tool_runs
Create Date: 2026-08-17 22:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a19_wf_runs'
down_revision: Union[str, Sequence[str], None] = 'a18_tool_runs'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('workflow_runs',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('workflow_id', sa.UUID(), nullable=False),
    sa.Column('workflow_version_id', sa.UUID(), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('input_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('output_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('error_message', sa.Text(), nullable=True),
    sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['workflow_id'], ['workflows.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['workflow_version_id'], ['workflow_versions.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workflow_runs_user_id'), 'workflow_runs', ['user_id'], unique=False)
    op.create_index(op.f('ix_workflow_runs_workflow_id'), 'workflow_runs', ['workflow_id'], unique=False)
    op.create_index(op.f('ix_workflow_runs_workflow_version_id'), 'workflow_runs', ['workflow_version_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_workflow_runs_workflow_version_id'), table_name='workflow_runs')
    op.drop_index(op.f('ix_workflow_runs_workflow_id'), table_name='workflow_runs')
    op.drop_index(op.f('ix_workflow_runs_user_id'), table_name='workflow_runs')
    op.drop_table('workflow_runs')
