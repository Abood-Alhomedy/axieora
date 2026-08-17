"""create workflow nodes table

Revision ID: a11_wf_nodes
Revises: a10_wf_versions
Create Date: 2026-08-17 22:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a11_wf_nodes'
down_revision: Union[str, Sequence[str], None] = 'a10_wf_versions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('workflow_nodes',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('workflow_version_id', sa.UUID(), nullable=False),
    sa.Column('node_id', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('type', sa.String(length=100), nullable=False),
    sa.Column('position_x', sa.Float(), nullable=False),
    sa.Column('position_y', sa.Float(), nullable=False),
    sa.Column('configuration', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['workflow_version_id'], ['workflow_versions.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('workflow_version_id', 'node_id', name='uq_workflow_version_node')
    )
    op.create_index(op.f('ix_workflow_nodes_workflow_version_id'), 'workflow_nodes', ['workflow_version_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_workflow_nodes_workflow_version_id'), table_name='workflow_nodes')
    op.drop_table('workflow_nodes')
