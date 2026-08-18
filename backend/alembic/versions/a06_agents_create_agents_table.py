"""create agents table

Revision ID: a06_agents
Revises: a05_tools
Create Date: 2026-08-17 22:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a06_agents'
down_revision: Union[str, Sequence[str], None] = 'a05_tools'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('agents',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('project_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('slug', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('instructions', sa.Text(), nullable=False),
    sa.Column('model', sa.String(length=255), nullable=True),
    sa.Column('temperature', sa.Float(), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('created_by', sa.UUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('project_id', 'slug', name='uq_agent_project_slug')
    )
    op.create_index(op.f('ix_agents_created_by'), 'agents', ['created_by'], unique=False)
    op.create_index(op.f('ix_agents_project_id'), 'agents', ['project_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_agents_project_id'), table_name='agents')
    op.drop_index(op.f('ix_agents_created_by'), table_name='agents')
    op.drop_table('agents')
