"""create workflow versions table

Revision ID: a10_wf_versions
Revises: a09_workflows
Create Date: 2026-08-17 22:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a10_wf_versions'
down_revision: Union[str, Sequence[str], None] = 'a09_workflows'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('workflow_versions',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('workflow_id', sa.UUID(), nullable=False),
    sa.Column('version_number', sa.Integer(), nullable=False),
    sa.Column('definition', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('created_by', sa.UUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['workflow_id'], ['workflows.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('workflow_id', 'version_number', name='uq_workflow_version')
    )
    op.create_index(op.f('ix_workflow_versions_created_by'), 'workflow_versions', ['created_by'], unique=False)
    op.create_index(op.f('ix_workflow_versions_workflow_id'), 'workflow_versions', ['workflow_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_workflow_versions_workflow_id'), table_name='workflow_versions')
    op.drop_index(op.f('ix_workflow_versions_created_by'), table_name='workflow_versions')
    op.drop_table('workflow_versions')
