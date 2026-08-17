"""create knowledge bases table

Revision ID: a28_knowledge_bases
Revises: a27_wk_invites
Create Date: 2026-08-17 22:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a28_knowledge_bases'
down_revision: Union[str, Sequence[str], None] = 'a27_wk_invites'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('knowledge_bases',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('workspace_id', sa.UUID(), nullable=False),
    sa.Column('project_id', sa.UUID(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('embedding_model', sa.String(length=255), nullable=True),
    sa.Column('created_by', sa.UUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_knowledge_bases_created_by'), 'knowledge_bases', ['created_by'], unique=False)
    op.create_index(op.f('ix_knowledge_bases_project_id'), 'knowledge_bases', ['project_id'], unique=False)
    op.create_index(op.f('ix_knowledge_bases_workspace_id'), 'knowledge_bases', ['workspace_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_knowledge_bases_workspace_id'), table_name='knowledge_bases')
    op.drop_index(op.f('ix_knowledge_bases_project_id'), table_name='knowledge_bases')
    op.drop_index(op.f('ix_knowledge_bases_created_by'), table_name='knowledge_bases')
    op.drop_table('knowledge_bases')
