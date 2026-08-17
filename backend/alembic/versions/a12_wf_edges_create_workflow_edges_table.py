"""create workflow edges table

Revision ID: a12_wf_edges
Revises: a11_wf_nodes
Create Date: 2026-08-17 22:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a12_wf_edges'
down_revision: Union[str, Sequence[str], None] = 'a11_wf_nodes'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('workflow_edges',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('workflow_version_id', sa.UUID(), nullable=False),
    sa.Column('source_node_id', sa.UUID(), nullable=False),
    sa.Column('target_node_id', sa.UUID(), nullable=False),
    sa.Column('condition', sa.Text(), nullable=True),
    sa.Column('edge_type', sa.String(length=100), nullable=False),
    sa.Column('configuration', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['source_node_id'], ['workflow_nodes.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['target_node_id'], ['workflow_nodes.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['workflow_version_id'], ['workflow_versions.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workflow_edges_source_node_id'), 'workflow_edges', ['source_node_id'], unique=False)
    op.create_index(op.f('ix_workflow_edges_target_node_id'), 'workflow_edges', ['target_node_id'], unique=False)
    op.create_index(op.f('ix_workflow_edges_workflow_version_id'), 'workflow_edges', ['workflow_version_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_workflow_edges_workflow_version_id'), table_name='workflow_edges')
    op.drop_index(op.f('ix_workflow_edges_target_node_id'), table_name='workflow_edges')
    op.drop_index(op.f('ix_workflow_edges_source_node_id'), table_name='workflow_edges')
    op.drop_table('workflow_edges')
