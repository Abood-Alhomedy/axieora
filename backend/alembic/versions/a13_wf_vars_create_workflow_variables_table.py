"""create workflow variables table

Revision ID: a13_wf_vars
Revises: a12_wf_edges
Create Date: 2026-08-17 22:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a13_wf_vars'
down_revision: Union[str, Sequence[str], None] = 'a12_wf_edges'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('workflow_variables',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('workflow_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('type', sa.String(length=100), nullable=False),
    sa.Column('default_value', sa.Text(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('required', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['workflow_id'], ['workflows.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('workflow_id', 'name', name='uq_workflow_variable_name')
    )
    op.create_index(op.f('ix_workflow_variables_workflow_id'), 'workflow_variables', ['workflow_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_workflow_variables_workflow_id'), table_name='workflow_variables')
    op.drop_table('workflow_variables')
